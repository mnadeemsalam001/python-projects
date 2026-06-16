# Google Index Checker

A Python script that checks whether your website pages are indexed on Google — using the **official Google Search Console URL Inspection API**. Results are tracked in an Excel file with a new date column added on every run, so you can monitor indexing status changes over time.

> **No scraping. No guessing.** This connects directly to Google's own data — the same data shown in Google Search Console when you manually inspect a URL.

---

## Features

- Uses the **Google Search Console URL Inspection API** — accurate, official data
- Checks multiple URLs in a single run
- **Tracks history in Excel** — each run adds a new date column so you can see changes week over week
- **Color-coded results** in Excel: green (indexed), red (not indexed), grey (error)
- Detailed status messages: know *why* a page isn't indexed, not just that it isn't
- Runs from any terminal location — always finds its files correctly
- Clean terminal output with a summary at the end

---

## Status Values Explained

| Status | Meaning |
|--------|---------|
| `Submitted and indexed` | ✅ Google has indexed this page |
| `Indexed, not submitted in sitemap` | ✅ Indexed but not in your sitemap |
| `Crawled - currently not indexed` | ⚠️ Google visited but chose not to index (check content quality) |
| `Discovered - currently not indexed` | ⚠️ Google knows it exists but hasn't crawled it yet |
| `URL is unknown to Google` | ❌ Google has never seen this URL — submit it in Search Console |
| `Excluded by 'noindex' tag` | ❌ Your page has a noindex tag blocking it |
| `Blocked by robots.txt` | ❌ Your robots.txt is blocking Google |
| `Soft 404` | ❌ Page returns 200 but looks like a missing page to Google |

---

## Project Structure

```
google-index-checker/
├── check_indexing.py              # Main script
├── Index_Tracker.xlsx               # Excel tracker (your URLs + results history)
├── credentials.json               # Google service account key (not committed to git)
├── requirements.txt               # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.8 or higher
- A website verified in **Google Search Console**
- A **Google Cloud** account (free)

---

## One-Time Setup

### Step 1 — Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click **Select a project** → **New Project**
3. Name it (e.g. `index-checker`) → **Create**

### Step 2 — Enable the Search Console API

1. Go to **APIs & Services → Library**
2. Search for **Google Search Console API** → click it → **Enable**

### Step 3 — Create a Service Account

1. Go to **APIs & Services → Credentials**
2. Click **+ Create Credentials → Service Account**
3. Name it (e.g. `index-checker-bot`) → **Create and Continue**
4. Skip the role selection → **Done**
5. Click the service account you just created → go to the **Keys** tab
6. Click **Add Key → Create new key → JSON → Create**
7. A `.json` file will download — rename it to `credentials.json` and place it in the project folder

### Step 4 — Grant Access in Search Console

This is the key step — it gives the service account permission to read your site's data.

1. Open `credentials.json` and copy the value of `"client_email"`  
   (looks like `index-checker-bot@your-project.iam.gserviceaccount.com`)
2. Go to [Google Search Console](https://search.google.com/search-console)
3. Select your website property
4. Go to **Settings → Users and permissions → Add User**
5. Paste the email → set permission to **Full** → **Add**

### Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install google-auth google-api-python-client openpyxl
```

---

## Setting Up Your Excel File

Create an Excel file (or export from Google Sheets) with the following structure:

| A | B |
|---|---|
| Page ID | URL |
| Home | https://yourdomain.com/ |
| About | https://yourdomain.com/about/ |
| Blog Post 1 | https://yourdomain.com/blog/post-title/ |

- **Column A** — any label/ID for your reference (page name, slug, etc.)
- **Column B** — the full URL to check (must start with `https://`)
- **Row 1** — headers (the script skips this row)
- **Row 2 onwards** — your data

Name your file and update `EXCEL_FILE` in the configuration section of `check_indexing.py`.

---

## Configuration

At the top of `check_indexing.py`, update these values to match your setup:

```python
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
EXCEL_FILE       = BASE_DIR / "Index_Tracker.xlsx"
SITE_URL         = "https://yourdomain.com/"   # must match your Search Console property exactly
```

> **Important:** `SITE_URL` must match your Search Console property exactly. Check the property URL in the top-left dropdown of Search Console — it may be `https://yourdomain.com/` or `sc-domain:yourdomain.com`.

---

## Usage

Run the script from any terminal:

```bash
python check_indexing.py
```

Or using the full path:

```bash
python "C:/path/to/google-index-checker/check_indexing.py"
```

**What happens on each run:**
1. The script reads all URLs from Column B of your Excel file
2. Queries Google Search Console for each URL's indexing status
3. Adds a new date column to the Excel file with today's date
4. Fills in the status for each URL with color coding
5. Saves the file and prints a summary

**Run it weekly** to build up a history of how your pages' indexing status changes over time.

---

## Sample Terminal Output

```
====================================================================
  GOOGLE INDEX CHECKER — yourdomain.com
  Date : 2026-06-15
====================================================================

Found 5 URL(s). Connecting to Search Console API...
Connected.

--------------------------------------------------------------------
[01/05] https://yourdomain.com/
        Submitted and indexed

[02/05] https://yourdomain.com/about/
        URL is unknown to Google

[03/05] https://yourdomain.com/services/
        Submitted and indexed

[04/05] https://yourdomain.com/blog/my-first-post/
        Crawled - currently not indexed

[05/05] https://yourdomain.com/contact/
        Submitted and indexed

--------------------------------------------------------------------
SUMMARY
  Indexed     : 3
  Not Indexed : 2
  Errors      : 0
  Total       : 5
--------------------------------------------------------------------

Results saved to: YourExcelFileName.xlsx
```

## Sample Excel Output

Each time you run the script, a new date column is added:

| Page ID | URL | 2026-06-15 | 2026-06-22 |
|---------|-----|------------|------------|
| Home | https://yourdomain.com/ | Submitted and indexed | Submitted and indexed |
| About | https://yourdomain.com/about/ | URL is unknown to Google | Submitted and indexed |
| Blog Post | https://yourdomain.com/blog/post/ | Crawled - currently not indexed | Submitted and indexed |

Cells are color-coded automatically — green for indexed, red for not indexed.

---

## Important Notes

- **Your site must be verified in Google Search Console** — the API only works for properties you own
- **`credentials.json` is sensitive** — never commit it to a public repository. It is already listed in `.gitignore`
- **API quota** — the URL Inspection API allows 2,000 requests per day and 600 per minute. Checking 30–100 URLs weekly is well within limits
- **Accuracy** — this is direct data from Google, not an estimate. The same result you would see manually inspecting a URL in Search Console

---

## Requirements

- Python 3.8+
- `google-auth`
- `google-api-python-client`
- `openpyxl`

---

## License

MIT License — free to use, modify, and distribute.
