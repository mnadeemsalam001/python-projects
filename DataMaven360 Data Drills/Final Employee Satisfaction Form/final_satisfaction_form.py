import pandas as pd
from pathlib import Path

# 1. Locate the CSV file in the same folder as this script
#    (this way it works regardless of the current working directory)
script_dir = Path(__file__).parent
file_path = script_dir / 'employee_satisfaction_survey.csv'

# 2. Read the CSV and parse the "Timestamp" column as actual datetime values
#    (without parse_dates, it would be read as plain text/object)
df = pd.read_csv(file_path, parse_dates=["Timestamp"])

# 3. Clean up the "Email" column
#    - .str.strip() removes leading/trailing spaces
#    - .str.lower() makes casing consistent (e.g., "John@X.com" -> "john@x.com")
#    This prevents the same person's email being treated as two different values
df["Email"] = df["Email"].str.strip().str.lower()

# 4. Isolate each employee's most recent response
#    - sort_values sorts by Email first, then by Timestamp (oldest to newest within each email)
#    - drop_duplicates keeps only one row per Email
#    - keep="last" ensures the row kept is the one with the latest Timestamp
#    - reset_index(drop=True) renumbers the rows cleanly after dropping duplicates
df_latest = (
    df.sort_values(["Email", "Timestamp"])
      .drop_duplicates(subset=["Email"], keep="last")
      .reset_index(drop=True)
)

# 5. Count how many employees fall into each satisfaction rating
#    (based only on each employee's latest response, thanks to step 4)
rating_counts = df_latest["Satisfaction"].value_counts()

print(rating_counts)