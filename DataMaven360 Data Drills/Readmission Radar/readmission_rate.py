import pandas as pd

df = pd.read_csv("D:\\Learning\\Python\\python-projects\\Maven Data Drills\\Readmission Radar\\inpatient_admissions.csv", parse_dates=["admission_date", "discharge_date"])

# Work per patient, sorted by admission date, so each discharge can be
# compared against that same patient's next admission.
df = df.sort_values(["patient_id", "admission_date"]).reset_index(drop=True)

# Next admission date for the same patient (NaT for a patient's last stay).
df["next_admission_date"] = df.groupby("patient_id")["admission_date"].shift(-1)

df["days_to_next_admission"] = (df["next_admission_date"] - df["discharge_date"]).dt.days

# Readmission window is 1-30 days after discharge, inclusive of day 30.
# (days_to_next_admission == 0 would mean admitted the same day as discharge,
# which the data doesn't produce here, but is excluded just in case since it's
# not a *readmission* in the usual clinical sense.)
df["is_30_day_readmission"] = df["days_to_next_admission"].between(1, 30)

total_discharges = len(df)
readmissions = df["is_30_day_readmission"].sum()
readmission_rate = readmissions / total_discharges

print(f"Total discharges:        {total_discharges}")
print(f"30-day readmissions:     {readmissions}")
print(f"30-day readmission rate: {readmission_rate:.2%}")