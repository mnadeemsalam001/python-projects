# Python Projects

A collection of reusable Python scripts for data processing, reporting, and automation.
Each script is self-contained and includes sample data so you can run it immediately.

---

## Scripts

### `report_formatter.py` — Professional Excel Report Formatter

Generates a polished, multi-sheet Excel workbook from a pandas DataFrame using **openpyxl**.
Includes a sample sales dataset so no external files are needed to get started.

**Features demonstrated:**
- Title bar, subtitle bar, and group headers (merged cells)
- Alternating row backgrounds
- Color-coded performance tier badges
- Positive / negative variance coloring (green / coral)
- Conditional formatting: color scale and data bars
- Excel SUM / AVERAGE formulas in the totals row
- Freeze panes

**Output:** `sample_report.xlsx` with two sheets — *Sales Report* and *Regional Summary*

**Install dependencies:**
```bash
pip install pandas openpyxl
```

**Run:**
```bash
python report_formatter.py
```

---

### `blog_scraper.py` — General-Purpose Blog / Website Scraper

Scrapes articles from any blog and saves each one as a clean Markdown file
with YAML front matter (title, date, URL, description, word count).
A CSV summary index is also produced.

**Two modes:**
- **Auto-discover** — point it at a blog index page; it finds all article links and scrapes them automatically
- **List mode** — provide a `.txt` file of URLs (one per line)

**Features demonstrated:**
- HTTP requests with a browser-like User-Agent header
- HTML parsing with BeautifulSoup (meta tag extraction, DOM traversal)
- Smart article body detection (walks the DOM to find the content container)
- HTML → Markdown conversion using `markdownify`
- YAML front matter generation
- Polite crawling (configurable delay between requests)
- Resume support — skips already-scraped files
- CSV summary index of all scraped articles
- CLI interface with `argparse` (`--url`, `--list`)

**Output:** One `.md` file per article + `_summary.csv` in the `articles/` folder

**Install dependencies:**
```bash
pip install requests beautifulsoup4 markdownify
```

**Three ways to run it:**

The script accepts optional arguments on the command line that control which URLs to scrape.

---

**Mode 1 — Auto-discover** *(no arguments)*
```bash
python blog_scraper.py
```
No extra input needed. The script reads `index_url` from the `CONFIG` block at the top of the file, crawls that page, finds all article links automatically, and scrapes them one by one.

Use this when you want to scrape an entire blog.

---

**Mode 2 — Single URL** *(`--url`)*
```bash
python blog_scraper.py --url https://blog.python.org/2026/05/python-3145-is-out
```
Scrapes exactly one page. Good for testing — try one article first before committing to scraping the whole site.

Use this to test the script or grab one specific page.

---

**Mode 3 — From a file** *(`--list`)*

Create a plain text file `urls.txt` with one URL per line:
```
https://blog.python.org/2026/05/python-3145-is-out
https://blog.python.org/2026/03/jit-on-track
https://blog.python.org/2026/04/rust-for-cpython-2026-04
```
Then run:
```bash
python blog_scraper.py --list urls.txt
```
The script reads your file and scrapes each URL in it.

Use this when you have a specific set of articles you want, not the whole blog.

---

In all three modes the output is the same — Markdown files saved to the `articles/` folder.
The only difference is how you tell the script which URLs to scrape.

> **Note:** Always check a site's `robots.txt` and Terms of Service before scraping.

---

## Requirements

- Python 3.8+
- Dependencies vary per script — each script lists its own `pip install` line at the top

---

## Contributing

Feel free to fork, adapt, and share. If you improve a script or add a new one, pull requests are welcome.
