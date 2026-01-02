"""
Remove deleted or unavailable videos which I can't get data for using youtube data api
4.26% (296 out of 6946) are unavailable and removed
"""
import pandas as pd

df = pd.read_csv("ywh_v8_channel_anonymized.csv")

df['watched_at'] = pd.to_datetime(df['watched_at'], errors='coerce')

valid_videos = df[
    df['channel'].notna() &
    df['duration_seconds'].notna()
].copy()

valid_videos.to_csv("ywh_v9_final.csv", index=False)

print("Original rows:", len(df))
print("Valid video rows:", len(valid_videos))
