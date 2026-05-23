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

## Requirements

- Python 3.8+
- Dependencies vary per script — each script lists its own `pip install` line at the top

---

## Contributing

Feel free to fork, adapt, and share. If you improve a script or add a new one, pull requests are welcome.
