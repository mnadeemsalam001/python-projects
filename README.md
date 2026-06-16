# Python Projects

A collection of self-contained Python scripts for data processing, reporting, automation, and desktop utilities.
Each project includes everything needed to run it immediately.

---

## Table of Contents

| # | Project | Description |
|---|---------|-------------|
| 1 | [Excel Report Formatter](#excel-formatter) | Generate polished multi-sheet Excel workbooks from a DataFrame |
| 2 | [Blog Scraper](#blog-scraper) | Scrape any blog and save articles as clean Markdown files |
| 3 | [Google Index Checker](#google-index-checker) | Track Google indexing status of your pages over time |
| 4 | [Image to WebP Converter](#image-to-webp) | GUI app to convert images to WebP with adjustable quality |

> Each project lives in its own folder. Navigate into the folder before running any script.


---

<a name="excel-formatter"></a>
### `excel-report-formatter/` — Professional Excel Report Formatter

Generates a polished, multi-sheet Excel workbook from a pandas DataFrame using **openpyxl**.
Includes a sample sales dataset so no external files are needed to get started.

**Features:**
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
cd excel-report-formatter
python excel_report_formatter.py
```

---

<a name="blog-scraper"></a>
### `blog-scraper/` — General-Purpose Blog / Website Scraper

Scrapes articles from any blog and saves each one as a clean Markdown file
with YAML front matter (title, date, URL, description, word count).
A CSV summary index is also produced.

**Two modes:**
- **Auto-discover** — point it at a blog index page; it finds all article links and scrapes them automatically
- **List mode** — provide a `.txt` file of URLs (one per line)

**Features:**
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

**Mode 1 — Auto-discover** *(no arguments)*
```bash
cd blog-scraper
python blog_scraper.py
```

**Mode 2 — Single URL**
```bash
python blog_scraper.py --url https://blog.python.org/2026/05/some-article
```

**Mode 3 — From a file**
```bash
python blog_scraper.py --list urls.txt
```

> **Note:** Always check a site's `robots.txt` and Terms of Service before scraping.

---

<a name="google-index-checker"></a>
### `google-index-checker/` — Google Index Status Checker

Checks whether your website pages are indexed on Google using the **official Google Search Console URL Inspection API** — the same data you see when you manually inspect a URL in Search Console. Results are tracked in an Excel file with a new date column added on every run, so you can monitor indexing changes over time.

**Features:**
- Google Search Console URL Inspection API with service account authentication
- Reading and writing Excel files with `openpyxl`
- Color-coded cells (green = indexed, red = not indexed)
- Historical tracking — each weekly run appends a new date column
- Graceful error handling and clear terminal output

**Output:** Color-coded Excel tracker with a running history of indexing status per URL

**Install dependencies:**
```bash
pip install google-auth google-api-python-client openpyxl
```

**Run:**
```bash
cd google-index-checker
python check_indexing.py
```

> **Note:** Requires a verified Google Search Console property and a service account key (`credentials.json`). See the [project README](google-index-checker/README.md) for the full setup guide.

---

<a name="image-to-webp"></a>
### `image-to-webp/` — Image to WebP Converter

A desktop GUI application that converts common image formats to WebP with adjustable quality and lossless mode. Built with **Tkinter** and **Pillow** — no browser or internet connection required.

![App Screenshot](screenshot.png)

**Features:**
- Supports PNG, JPEG, BMP, TIFF, GIF, ICO, and HEIC/HEIF (with optional plugin)
- Quality slider (1–100) with live hints
- Lossless mode for pixel-perfect output
- Batch conversion — add individual files or an entire folder at once
- Custom output directory or save alongside originals
- Progress bar with per-file status
- Transparency / alpha channel handled correctly

**Install dependencies:**
```bash
pip install pillow
```

For HEIC/HEIF support (iPhone photos):
```bash
pip install pillow-heif
```

**Run:**
```bash
cd image-to-webp
python image_to_webp.py
```

---

## Requirements

- Python 3.10+
- Dependencies vary per project — each project lists its own `pip install` line above

---

## Contributing

Feel free to fork, adapt, and share. If you improve a script or add a new one, pull requests are welcome.
