"""
Remove live streams
"""

import pandas as pd

# CONFIG
INPUT_CSV = "ywh_deduplicated.csv"
OUTPUT_CSV = "ywh_v3_livestreams_removed.csv"
DURATION_THRESHOLD = 3600  # seconds

df = pd.read_csv(INPUT_CSV)

df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

mask = (
    df["title"]
      .astype(str)
      .str.lower()
      .str.contains(r"live|stream", regex=True, na=False)
    &
    (df["duration_seconds"] > DURATION_THRESHOLD)
)

matched = df.loc[mask, ["title", "duration_seconds", "channel"]]
print(f"Rows matched (to be removed): {len(matched)}")
print(matched.sort_values("duration_seconds", ascending=False).head(10))

# Remove rows
df_cleaned = df.loc[~mask].copy()

# Save
df_cleaned.to_csv(OUTPUT_CSV, index=False)

print(f"Saved cleaned file → {OUTPUT_CSV}")
print(f"Original rows: {len(df)}")
print(f"After removal: {len(df_cleaned)}")
