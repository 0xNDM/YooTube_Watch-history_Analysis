"""
Remove long un watched videos (I checked the videos on SQL and created this condition)
Extract only 2025 data
"""
import pandas as pd

INPUT_CSV = "ywh_v3_livestreams_removed.csv"
OUTPUT_CSV = "ywh_v4_videos_2025.csv"

df = pd.read_csv(INPUT_CSV)

df.columns = df.columns.str.strip().str.lower()

# Convert types
df["watched_at"] = pd.to_datetime(df["watched_at"], errors="coerce")
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

# Keep ONLY 2025
df = df[df["watched_at"].dt.year == 2025].copy()

# Whitelist channels
whitelist = [
    "My Lesson",
    "Programming with Mosh"
]

# Remove Condition (remove if not in whitelist channels or channel name doesn't contain podcast or good)
long_video = df["duration_seconds"] > 12000
not_whitelisted = ~df["channel"].isin(whitelist)
no_keywords = ~df["channel"].astype(str).str.contains(
    r"podcast|good",
    case=False,
    regex=True,
    na=False
)

remove_mask = long_video & not_whitelisted & no_keywords

# Apply removal
df_clean = df[~remove_mask].copy()

# Sort chronologically
df_clean = df_clean.sort_values("watched_at").reset_index(drop=True)

# Save
df_clean.to_csv(OUTPUT_CSV, index=False)

print("✅ Done")
print(f"2025 rows before: {len(df)}")
print(f"Removed rows     : {remove_mask.sum()}")
print(f"Rows after       : {len(df_clean)}")
