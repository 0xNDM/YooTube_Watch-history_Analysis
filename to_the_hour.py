"""
floor watched_at and publised_at datetime to the hour 
"""

import pandas as pd


INPUT_CSV = "ywh_v5_datetime.csv"
OUTPUT_CSV = "ywh_v6_floored_datetime.csv"


df = pd.read_csv(INPUT_CSV)

df["watched_at"] = pd.to_datetime(df["watched_at"], errors="coerce")
df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")

# Floor datetime to the hour
df["watched_at"] = df["watched_at"].dt.floor("h")
df["published_at"] = df["published_at"].dt.floor("h")

# Save 
df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved hourly-rounded file to: {OUTPUT_CSV}")
