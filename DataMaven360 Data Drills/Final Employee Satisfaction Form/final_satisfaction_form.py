import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent
file_path = script_dir / 'employee_satisfaction_survey.csv'

df = pd.read_csv(file_path,parse_dates=["Timestamp"]) 

df_latest = df.sort_values(["Email","Timestamp"]).drop_duplicates(subset=["Email"], keep="last").reset_index(drop=True)

rating_counts = df_latest["Satisfaction"].value_counts()

print(rating_counts)