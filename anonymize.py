"""
Anonymize data drop title, url, video_id
drop un neccessary columns like category id 
create new video ids that auto increment
"""

import pandas as pd

df = pd.read_csv("ywh_v6_floored_datetime.csv")

df["watched_at"] = pd.to_datetime(df["watched_at"], errors="coerce")

df = df.sort_values("watched_at").reset_index(drop=True)

# Generate new anonymized video_id
df.insert(
    0,
    "new_video_id",
    [f"vid_{i:05d}" for i in range(1, len(df) + 1)]
)

columns_to_drop = ["title", "url", "video_id", "category_id"]
df = df.drop(columns=columns_to_drop, errors="ignore")

final_columns = [
    "new_video_id",
    "channel",
    "watched_at",
    "published_at",
    "category",
    "duration_seconds",
    "views",
    "likes",
    "type",
    "account"
]

df = df[final_columns]

df.to_csv("ywh_v7_anonymized.csv", index=False)
