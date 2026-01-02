"""
Anonymize channels that are not on the top 10 by watch hour or count
"""

import pandas as pd

df = pd.read_csv("ywh_v7_anonymized.csv")

df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

top_by_hours = (
    df.groupby("channel", as_index=False)["duration_seconds"]
    .sum()
    .sort_values("duration_seconds", ascending=False)
    .head(10)["channel"]
)

top_by_count = df["channel"].value_counts().head(10).index

keep_channels = set(top_by_hours).union(set(top_by_count))

other_channels = sorted(
    [ch for ch in df["channel"].unique() 
     if ch not in keep_channels and pd.notna(ch) and ch != ""]
)

# Create anonymized mapping
anon_map = {ch: f"channel_{i:04d}" for i, ch in enumerate(other_channels, start=1)}

def anonymize_channel(ch):
    if pd.isna(ch) or ch == "":
        return ""  # leave missing channels empty
    elif ch in keep_channels:
        return ch  # keep top channels
    else:
        return anon_map[ch]  # anonymize others

df["channel"] = df["channel"].apply(anonymize_channel)


df.to_csv("ywh_v8_channel_anonymized.csv", index=False)
