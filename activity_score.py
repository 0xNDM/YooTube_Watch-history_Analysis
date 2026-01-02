"""
Generate activity score and activity level using percentile of watch hour and watch frequency
"""

import pandas as pd
import numpy as np

df = pd.read_csv("ywh_v9_final.csv")

df["watched_at"] = pd.to_datetime(df["watched_at"]).dt.normalize()

# Aggregate
daily_stats = df.groupby("watched_at").agg(
    daily_watch_hours=("duration_seconds", lambda x: x.sum() / 3600),
    watch_frequency=("video_id", "count"),
)

# Create the full range as a proper DatetimeIndex
full_range = pd.date_range(start="2025-01-01", end="2025-12-31")

daily_report = daily_stats.reindex(full_range, fill_value=0)
daily_report.index.name = "date"

# Calculate Weighted Score (95th Percentile)
p95_hours = daily_report["daily_watch_hours"].quantile(0.95)
p95_freq = daily_report["watch_frequency"].quantile(0.95)

hour_score = (daily_report["daily_watch_hours"] / p95_hours).clip(upper=1.0)
freq_score = (daily_report["watch_frequency"] / p95_freq).clip(upper=1.0)

# Final 70/30 weighted score
daily_report["activity_score"] = (0.7 * hour_score) + (0.3 * freq_score)

daily_report["daily_watch_hours"] = daily_report["daily_watch_hours"].round(2)
daily_report["activity_score"] = daily_report["activity_score"].round(2)

daily_report["activity_level"] = np.select(
    [
        daily_report["activity_score"] == 0,
        (daily_report["activity_score"] > 0) & (daily_report["activity_score"] < 0.15),
        (daily_report["activity_score"] >= 0.15) & (daily_report["activity_score"] < 0.4),
        daily_report["activity_score"] >= 0.4
    ],
    ["None", "Low", "Medium", "High"],
    default="None"   
)

daily_report.to_csv("activity_score.csv")


