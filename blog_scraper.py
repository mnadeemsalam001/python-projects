"""
================================================================================
Blog Scraper  —  General-Purpose Web Article Scraper
================================================================================
Author : Muhammad Nadeem Salam
Version: 1.0

Description:
    Scrapes articles from any blog or website and saves each one as a clean
    Markdown file with YAML front matter (title, date, URL, description,
    word count).  A CSV summary index is also produced.

Two modes:
    DISCOVER mode  — Point it at a blog index/listing page and it finds all
                     article links automatically, then scrapes each one.

    LIST mode      — Provide a plain-text file of URLs (one per line) and it
                     scrapes only those pages.

What you get per article:
    articles/
    ├── my-first-post.md        ← clean Markdown + YAML front matter
    ├── another-article.md
    └── _summary.csv            ← index of all scraped articles

Usage:
    python blog_scraper.py                         # uses CONFIG below
    python blog_scraper.py --url  https://...      # scrape one URL
    python blog_scraper.py --list urls.txt         # scrape from a file

Requirements:
    pip install requests beautifulsoup4 markdownify

IMPORTANT:
    Always check a site's robots.txt and Terms of Service before scraping.
    Use a reasonable crawl delay (1-2 seconds) to avoid overloading servers.
    Example robots.txt: https://example.com/robots.txt

================================================================================
"""

import os
import re
import csv
import time
import argparse
from datetime import datetime
from urllib.parse import urljoin, urlparse

import warnings
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import markdownify

# Suppress BeautifulSoup warning when it encounters an XML feed (e.g. rss.xml)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


# ================================================================================
# CONFIG  —  Change these settings to match your target site
# ================================================================================

CONFIG = {
    # The blog's index/listing page. The scraper will find all article links here.
    "index_url": "https://blog.python.org/",

    # CSS selector used to identify article links on the index page.
    # Common values: "article a", "h2 a", ".post-title a", "a.entry-title"
    "link_selector": "a",

    # Only keep links whose URL path STARTS WITH this string.
    # Helps filter out nav/footer links.
    # Examples: "/blog/", "/articles/", "/posts/", "/20" (for year-based URLs like /2024/...)
    # Set to "" to keep all same-domain links.
    "link_filter": "/20",

    # How many articles to scrape.  Set to None for no limit.
    "max_articles": 10,

    # Seconds to wait between requests (be polite to the server).
    "delay": 1.5,

    # Folder where Markdown files will be saved.
    "output_dir": "articles",

    # Phrases that signal the end of the article body (footer / CTA junk).
    # Anything after the first matching phrase will be removed.
    "stop_phrases": [
        "Subscribe to our newsletter",
        "You might also like",
        "Related articles",
        "Share this post",
        "Leave a comment",
    ],
}

# Browser-like User-Agent header so the server accepts the request.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


# ================================================================================
# HELPER FUNCTIONS
# ================================================================================

def slugify(url: str) -> str:
    """Convert a URL into a safe filename (no special characters)."""
    path = urlparse(url).path.strip("/")
    slug = re.sub(r"[^\w\-]", "_", path)
    slug = re.sub(r"_+", "_", slug)          # collapse multiple underscores
    return slug[:120] or "article"


def extract_meta(soup: BeautifulSoup, url: str) -> dict:
    """
    Pull title, publish date, and description from a page's meta tags.

    Priority order:
        1. Open Graph meta tags  (og:title, og:description)
        2. Standard meta tags    (name="description")
        3. <title> tag / visible text fallback
    """
    def og(prop):
        tag = soup.find("meta", property=f"og:{prop}")
        return tag["content"].strip() if tag and tag.get("content") else ""

    def meta_name(name):
        tag = soup.find("meta", attrs={"name": name})
        return tag["content"].strip() if tag and tag.get("content") else ""

    # Title
    title = (og("title")
             or meta_name("title")
             or (soup.title.get_text(strip=True) if soup.title else "")
             or url)

    # Description
    description = og("description") or meta_name("description")

    # Date — try structured meta tags first, then scan visible text
    date = ""
    for prop in ("article:published_time", "article:modified_time",
                 "og:updated_time", "datePublished"):
        tag = soup.find("meta", property=prop) or soup.find("meta", attrs={"name": prop})
        if tag and tag.get("content"):
            raw = tag["content"][:10]          # keep YYYY-MM-DD part only
            try:
                date = datetime.strptime(raw, "%Y-%m-%d").strftime("%B %d, %Y")
            except ValueError:
                date = raw
            break

    # Date fallback — look for a "Month DD, YYYY" pattern in visible text
    if not date:
        match = re.search(
            r"(January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+\d{1,2},?\s+\d{4}",
            soup.get_text()
        )
        if match:
            date = match.group(0)

    return {"title": title, "description": description, "date": date}


def discover_article_urls(session: requests.Session, index_url: str,
                          selector: str, link_filter: str,
                          max_count: int) -> list:
    """
    Crawl a blog index page and return a list of article URLs found on it.

    Steps:
        1. Download the index page HTML
        2. Find all <a> tags matching the CSS selector
        3. Convert relative links to absolute URLs
        4. Filter to same-domain links containing link_filter in the path
        5. Remove duplicates while preserving order
    """
    print(f"Discovering articles from: {index_url}")
    try:
        resp = session.get(index_url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  [ERROR] Could not fetch index page — {exc}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    base_domain = urlparse(index_url).netloc
    seen  = set()
    urls  = []

    for tag in soup.select(selector):
        href = tag.get("href", "")
        if not href or href.startswith(("#", "mailto:", "javascript:")):
            continue

        full_url = urljoin(index_url, href).split("#")[0]   # drop anchor fragments

        # Stay on the same domain
        if urlparse(full_url).netloc != base_domain:
            continue

        # Apply path filter — URL path must start with the filter string
        if link_filter and not urlparse(full_url).path.startswith(link_filter):
            continue

        # Skip the index page itself
        if full_url.rstrip("/") == index_url.rstrip("/"):
            continue

        if full_url not in seen:
            seen.add(full_url)
            urls.append(full_url)

        if max_count and len(urls) >= max_count:
            break

    print(f"  Found {len(urls)} article link(s)")
    return urls


def find_article_node(soup: BeautifulSoup):
    """
    Locate the DOM node that holds the article body.

    Strategy:
        - Find the <h1> (article title)
        - Walk up its parent chain looking for a container
          that holds more than 1000 characters of text
          (enough to be the full article, not just the heading)
        - Stop at <body> or after 6 levels if nothing found
    """
    # Also try semantic article/main tags first
    for tag_name in ("article", "main"):
        node = soup.find(tag_name)
        if node and len(node.get_text()) > 1000:
            return node

    h1 = soup.find("h1")
    if not h1:
        return soup.find("body")

    candidate = h1.parent
    for _ in range(6):
        if candidate is None or candidate.name in ("body", "html"):
            break
        if len(candidate.get_text()) > 1000:
            return candidate
        candidate = candidate.parent

    return h1.parent


def remove_clutter(node) -> None:
    """
    Strip navigation, ads, footers, and scripts from the article node in-place.
    Modifies the node directly — no return value needed.
    """
    for tag in node.find_all(["nav", "header", "footer",
                               "script", "style", "noscript", "iframe"]):
        tag.decompose()

    # Remove common boilerplate link/button text
    boilerplate = {
        "back to blog", "home", "about", "pricing", "faq",
        "get started", "sign up", "subscribe", "explore more",
        "blog", "contact", "support", "read more",
    }
    for tag in node.find_all(["a", "button"]):
        if tag.get_text(strip=True).lower() in boilerplate:
            tag.decompose()


def to_markdown(node) -> str:
    """
    Convert a BeautifulSoup node to clean, readable Markdown.

    Settings used:
        ATX headings    → # H1  ## H2  etc. (instead of underline style)
        Bullets         → -  (consistent dash bullets)
        Strip images    → removes <img> tags (keeps alt text)
        Strip links     → removes <a> hrefs (keeps link text)
    """
    md = markdownify.markdownify(
        str(node),
        heading_style=markdownify.ATX,
        bullets="-",
        strip=["img", "a"],          # drop images and hyperlinks, keep their text
        newline_style="backslash",
    )
    md = re.sub(r"\n{3,}", "\n\n", md)   # collapse 3+ blank lines into 2
    return md.strip()


def trim_footer(md: str, stop_phrases: list) -> str:
    """Remove everything from the first footer/CTA phrase onwards."""
    for phrase in stop_phrases:
        idx = md.find(phrase)
        if idx != -1:
            md = md[:idx]
    return md.strip()


# ================================================================================
# SCRAPE + SAVE
# ================================================================================

def scrape_url(session: requests.Session, url: str, stop_phrases: list) -> dict | None:
    """
    Download a single page and extract the article content.

    Returns a dict with: url, slug, title, date, description,
                         body_markdown, word_count
    Returns None on any network or parsing error.
    """
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  [ERROR] {exc}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    meta = extract_meta(soup, url)

    article_node = find_article_node(soup)
    if article_node is None:
        print("  [WARN] No article body found — saving empty content")
        body_md = ""
    else:
        remove_clutter(article_node)
        body_md = to_markdown(article_node)
        body_md = trim_footer(body_md, stop_phrases)

    return {
        "url":           url,
        "slug":          slugify(url),
        "title":         meta["title"],
        "date":          meta["date"],
        "description":   meta["description"],
        "body_markdown": body_md,
        "word_count":    len(body_md.split()),
    }


def save_as_markdown(data: dict, directory: str) -> str:
    """
    Save article data as a Markdown file with YAML front matter.

    YAML front matter looks like:
        ---
        title: "My Article Title"
        date:  "January 15, 2025"
        url:   "https://example.com/my-article"
        ---
    """
    filepath = os.path.join(directory, data["slug"] + ".md")
    with open(filepath, "w", encoding="utf-8") as f:
        # Write YAML front matter block
        f.write("---\n")
        f.write(f'title:       "{data["title"].replace(chr(34), chr(39))}"\n')
        f.write(f'date:        "{data["date"]}"\n')
        f.write(f'url:         "{data["url"]}"\n')
        f.write(f'description: "{data["description"].replace(chr(34), chr(39))}"\n')
        f.write(f'word_count:  {data["word_count"]}\n')
        f.write("---\n\n")
        # Write article body
        f.write(data["body_markdown"])
    return filepath


# ================================================================================
# MAIN
# ================================================================================

def run(urls: list, config: dict):
    """Scrape a list of URLs and save results to disk."""
    os.makedirs(config["output_dir"], exist_ok=True)
    summary_rows = []
    success = 0
    failed  = 0

    with requests.Session() as session:
        total = len(urls)
        for i, url in enumerate(urls, 1):
            print(f"[{i:02d}/{total:02d}] {url}")

            # Skip if already scraped (resume support)
            slug     = slugify(url)
            out_path = os.path.join(config["output_dir"], slug + ".md")
            if os.path.exists(out_path):
                print("         already scraped — skipping")
                success += 1
                continue

            data = scrape_url(session, url, config["stop_phrases"])

            if data:
                filepath = save_as_markdown(data, config["output_dir"])
                summary_rows.append({
                    "index":      i,
                    "title":      data["title"],
                    "date":       data["date"],
                    "url":        data["url"],
                    "word_count": data["word_count"],
                    "file":       os.path.basename(filepath),
                })
                print(f"         saved: {filepath}  ({data['word_count']} words)")
                success += 1
            else:
                print("         failed — skipped")
                failed += 1

            if i < total:
                time.sleep(config["delay"])

    # Write CSV summary index
    if summary_rows:
        csv_path = os.path.join(config["output_dir"], "_summary.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["index", "title", "date", "url", "word_count", "file"]
            )
            writer.writeheader()
            writer.writerows(summary_rows)
        print(f"\nSummary index saved: {csv_path}")

    print(f"\nDone.  {success} saved,  {failed} failed  "
          f"(output folder: '{config['output_dir']}')")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape blog articles and save them as Markdown files."
    )
    parser.add_argument(
        "--url",
        help="Scrape a single URL (overrides CONFIG index_url)",
    )
    parser.add_argument(
        "--list",
        metavar="FILE",
        help="Path to a .txt file with one URL per line",
    )
    args = parser.parse_args()

    if args.url:
        # Single-URL mode
        urls = [args.url.strip()]

    elif args.list:
        # File-of-URLs mode
        with open(args.list, encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"Loaded {len(urls)} URLs from {args.list}")

    else:
        # Auto-discover mode — crawl the index page in CONFIG
        with requests.Session() as session:
            urls = discover_article_urls(
                session,
                index_url   = CONFIG["index_url"],
                selector    = CONFIG["link_selector"],
                link_filter = CONFIG["link_filter"],
                max_count   = CONFIG["max_articles"] or 0,
            )

    if not urls:
        print("No URLs to scrape. Check your CONFIG or provide --url / --list.")
        return

    run(urls, CONFIG)


if __name__ == "__main__":
    main()
