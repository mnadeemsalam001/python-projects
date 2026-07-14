# Readmission Radar

Calculates a hospital's **30-day readmission rate** from a raw list of inpatient
discharge records.

## Project Background

Hospitals track how often discharged patients end up back in the hospital
shortly after leaving, since a high **readmission rate** can point to poor
discharge planning or care quality. This project analyzes a dataset of
inpatient stays for a small hospital and calculates that rate.

## Dataset

**File:** `inpatient_admissions.csv`

623 inpatient stay records. Each row is one discharge, with these columns:

| Column           | Description                                   |
|------------------|------------------------------------------------|
| `admission_id`   | Unique ID for the stay                          |
| `patient_id`     | ID of the patient (a patient can appear multiple times) |
| `admission_date` | Date the patient was admitted                   |
| `discharge_date` | Date the patient was discharged                 |

## Task / Requirements

Calculate the hospital's 30-day readmission rate:

- A discharge counts as a **30-day readmission** when the same patient is
  admitted again within 30 days of their discharge date.
- **Day 30 is included** in the readmission window (i.e. the window is
  discharge date + 1 day through discharge date + 30 days, inclusive).
- Assume every record in the dataset has had a full 30-day follow-up
  window (no need to exclude any discharges just because they're near the
  end of the dataset's date range).

**Result:** 232 readmissions out of 623 discharges → **37.24%** readmission rate.

## How to Run

```bash
python readmission_rate.py
```

This prints the total discharge count, the number of 30-day readmissions,
and the readmission rate.

## Requirements

- Python 3
- [pandas](https://pandas.pydata.org/) (`pip install pandas`)

## Code Walkthrough (line by line)

This section explains the script for anyone new to Python.

### Line 1 — `import pandas as pd`

Python doesn't know how to work with spreadsheets/CSVs by default. **pandas**
is a library (pre-written code someone else wrote) that is the standard tool
for working with tabular data (rows and columns) in Python. `import` loads
that library into the script. `as pd` gives it a shorthand nickname, so
instead of typing `pandas.read_csv(...)` everywhere, you type `pd.read_csv(...)`.
This is just a naming convention almost everyone follows.

### Line 3 — reading the CSV

```python
df = pd.read_csv("...\\inpatient_admissions.csv", parse_dates=["admission_date", "discharge_date"])
```

- `pd.read_csv(...)` opens a CSV file and loads it into a **DataFrame** —
  pandas' name for a table with rows and columns, similar to an Excel sheet.
  Each column has a name (`patient_id`, `admission_date`, etc.) and every row
  is one record.
- `df = ` stores that table in a variable named `df` (short for "DataFrame" —
  just a convention, it could be named anything).
- The file path uses double backslashes (`\\`) because in Python a single
  backslash starts an "escape sequence" (e.g. `\n` means newline). Doubling
  it (`\\`) tells Python "this is a literal backslash, not a special code."
- `parse_dates=["admission_date", "discharge_date"]` — by default, everything
  read from a CSV is treated as plain text (strings). This argument tells
  pandas "these two columns actually contain dates — convert them into real
  date objects." Without this, `"2015-01-07"` would just be a piece of text
  and you couldn't do date math on it (like subtracting one date from
  another). With it, pandas understands the calendar and lets you calculate
  things like "how many days between these two dates?"

### Line 7 — sorting the data

```python
df = df.sort_values(["patient_id", "admission_date"]).reset_index(drop=True)
```

- `.sort_values([...])` reorders the rows of the table. Passing a list of two
  column names means "sort by `patient_id` first, and for rows with the same
  patient, sort those by `admission_date`." The effect: all of one patient's
  stays are grouped together, in chronological order — stay 1, stay 2, stay
  3, etc.
- This is needed because, to figure out if a patient came back within 30
  days, we need to know, for each stay, what their *next* stay was. That only
  works if the rows are already in time order per patient.
- `.reset_index(drop=True)` — every DataFrame has an "index," a hidden
  row-number label on the left side. After sorting, the original row numbers
  get shuffled out of order (e.g. 5, 12, 3, 47...). `reset_index` renumbers
  them cleanly as 0, 1, 2, 3... `drop=True` means "throw away the old jumbled
  index, don't keep it as a new column." This is just tidying up — it
  doesn't change any of the actual data.
- `df = df.sort_values(...).reset_index(...)` — both operations are "chained"
  with a dot, and the result is saved back into `df`, replacing the old
  unsorted table.

### Comments (lines starting with `#`)

Any line starting with `#` is a **comment** — a plain English note for
humans reading the code. Python completely ignores comments; they don't run
or affect the program. They exist purely to explain *why* the code does
something, since that's not always obvious just from reading the code
itself.

### Line 10 — finding each patient's next admission

```python
df["next_admission_date"] = df.groupby("patient_id")["admission_date"].shift(-1)
```

- `df["next_admission_date"] = ...` creates a **brand new column** in the
  table called `next_admission_date`, filled with whatever is on the right
  side of the `=`. In pandas, `df["some_name"] = ...` is how you add or
  overwrite a column.
- `df.groupby("patient_id")` splits the whole table into mini-tables, one per
  patient. Think of it as putting all of patient P0092's rows in one pile,
  all of P0070's rows in another pile, and so on. It's a temporary grouping
  that other operations then work on — it doesn't create a separate visible
  table.
- `["admission_date"]` — within each patient's pile, we only care about the
  `admission_date` column for this step.
- `.shift(-1)` is the key trick. "Shift" moves values up or down within a
  column. `shift(-1)` moves every value **up by one row** (i.e., pulls the
  *next* row's value into the *current* row). So for a given row, `shift(-1)`
  gives you "the value from the row right after this one." Because this
  happens after `groupby("patient_id")`, the shifting happens *separately
  within each patient's group* — a patient's data never "leaks" into another
  patient's shifted values.
- Put together: for every stay, this line looks up "this same patient's next
  admission date" and stores it in the new column. If a stay is a patient's
  **last** one in the dataset, there's no "next" row to pull from, so pandas
  fills that with `NaT` (pandas' version of "no date"/blank).

### Line 12 — calculating the gap in days

```python
df["days_to_next_admission"] = (df["next_admission_date"] - df["discharge_date"]).dt.days
```

- Creates a new column, `days_to_next_admission`.
- `df["next_admission_date"] - df["discharge_date"]` — because both columns
  hold real dates (thanks to `parse_dates` earlier), pandas lets you literally
  subtract one date column from another. The result isn't a plain number —
  it's a special pandas type called a **Timedelta**, representing a
  *duration* (e.g., "23 days" or "5 days, 3 hours").
- `.dt.days` — `.dt` is pandas' way of saying "treat this as date/time data
  and give me access to date-related properties." `.days` extracts just the
  whole number of days from that duration, giving a plain integer like `23`.
- So this line answers: "how many days passed between this discharge and
  this patient's next admission?" If there's no next admission
  (`next_admission_date` is `NaT`), the result is also blank (`NaN`, "Not a
  Number") rather than an error.

### Line 18 — flagging readmissions

```python
df["is_30_day_readmission"] = df["days_to_next_admission"].between(1, 30)
```

- New column: `is_30_day_readmission`.
- `.between(1, 30)` checks, for every row, whether the value in
  `days_to_next_admission` falls between 1 and 30, **inclusive of both
  ends**. A gap of exactly 30 days counts as "yes," matching the requirement
  that day 30 is included. A gap of 0 (same day), anything above 30, or a
  blank (no next admission), counts as "no."
- The result is a column of `True`/`False` values — one per row, answering
  "did this particular discharge turn into a 30-day readmission?"

### Lines 20-22 — computing the rate

```python
total_discharges = len(df)
readmissions = df["is_30_day_readmission"].sum()
readmission_rate = readmissions / total_discharges
```

- `len(df)` is a built-in Python function meaning "how many items are in
  this?" For a DataFrame, that means "how many rows are there?" — i.e., the
  total number of discharges (623). Stored in `total_discharges`.
- `df["is_30_day_readmission"].sum()` — a neat trick: in Python, `True`
  behaves like the number `1` and `False` behaves like `0`. Calling `.sum()`
  on a column of `True`/`False` values just counts how many `True`s there
  are — i.e., the total number of readmissions. Stored in `readmissions`.
- `readmissions / total_discharges` — plain division, giving the readmission
  rate as a decimal fraction (e.g., `0.3724`), stored in `readmission_rate`.

### Lines 24-26 — printing the results

```python
print(f"Total discharges:        {total_discharges}")
print(f"30-day readmissions:     {readmissions}")
print(f"30-day readmission rate: {readmission_rate:.2%}")
```

- `print(...)` displays text to the screen/console.
- The `f"..."` is an **f-string** (formatted string). Putting `f` right
  before the quotes lets you embed variables directly inside the text using
  curly braces `{}`. So `f"Total discharges: {total_discharges}"`
  automatically substitutes in whatever number is stored in
  `total_discharges` — no manual string-joining needed.
- `{readmission_rate:.2%}` is a special formatting instruction: `%` tells it
  to display the number as a percentage (multiplying by 100 and adding a `%`
  sign), and `.2` tells it to show 2 digits after the decimal point. So
  `0.3724` becomes `37.24%`.

## Big-Picture Summary

The script reads the CSV into a table, sorts it so each patient's visits are
in date order, looks ahead to find each patient's *next* admission, measures
the gap in days between a discharge and that next admission, flags any gap
of 1-30 days as a readmission, then counts and divides to get the final
rate — which it prints out nicely formatted.
