"""
Merge the 2 accounts CSVs Main and Educational Youtube accounts
"""

import pandas as pd

# Input files
csv_main = "youtube_history.csv"
csv_edu = "youtube_history_2.csv"

# Output file
output_csv = "combined_youtube_watch_history.csv"

df_main = pd.read_csv(csv_main)
df_edu = pd.read_csv(csv_edu)

# Add account column
df_main["account"] = "Main"
df_edu["account"] = "Educational"

cols_main = set(df_main.columns)
cols_edu = set(df_edu.columns)

if cols_main != cols_edu:
    raise ValueError(
        f"Column mismatch:\n"
        f"Main only: {cols_main - cols_edu}\n"
        f"Educational only: {cols_edu - cols_main}"
    )

# Merge
df_merged = pd.concat([df_main, df_edu], ignore_index=True)

df_merged.to_csv(output_csv, index=False, encoding="utf-8")

print(f"Merged CSV saved as: {output_csv}")
print(f"Total rows: {len(df_merged)}")
