"""
Deduplicate non-music videos by title 
"""

import pandas as pd

INPUT_CSV = "ywh_v1_combined_csvs.csv"
OUTPUT_CSV = "ywh_v2_deduplicated.csv"

df = pd.read_csv(INPUT_CSV)

df["watched_at"] = pd.to_datetime(df["watched_at"], errors="coerce")

# Normalize title
df["title_norm"] = (
    df["title"]
    .fillna("")
    .str.strip()
    .str.lower()
)

# Normalize category
df["category_norm"] = (
    df["category"]
    .fillna("")
    .str.strip()
    .str.lower()
)

# Split music vs non-music
music_df = df[df["category_norm"] == "music"]
non_music_df = df[df["category_norm"] != "music"]

# Deduplicate non-music by TITLE
non_music_dedup = (
    non_music_df
    .sort_values("watched_at")
    .drop_duplicates(subset=["title_norm"], keep="last")
)

final_df = pd.concat([music_df, non_music_dedup], ignore_index=True)

final_df = final_df.sort_values("watched_at")

# Drop helper columns
final_df = final_df.drop(columns=["title_norm", "category_norm"])


final_df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved → {OUTPUT_CSV}")
print(f"Original rows: {len(df)}")
print(f"After deduplication: {len(final_df)}")
