"""
Drop published_at, views, likes, account
Give more expressive names for type
Create local hour of day column
Create day of week column (this Still use the previous GMT because I count late night for the previous day)
"""

import pandas as pd

df = pd.read_csv("ywh_v9_final.csv")

df["watched_at"] = pd.to_datetime(df["watched_at"])

df = df.drop(columns=["published_at", "views", "likes", "account"], errors="ignore")

df["type"] = df["type"].replace({
    "video": "Long form",
    "short": "Short"
})

# hour_of_day_local (GMT +3, HH:00)
df["hour_of_day_local"] = (
    df["watched_at"] + pd.Timedelta(hours=3)
).dt.strftime("%H:00")

# day of week
df["day_of_week"] = df["watched_at"].dt.day_name()

df.to_csv("ywh_final.csv", index=False)

print("Cleaning complete. File saved as ywh_final.csv")
