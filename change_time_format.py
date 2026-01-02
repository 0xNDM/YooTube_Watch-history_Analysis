"""
Change date and time format to sql compatible datetime
"""

import csv
from datetime import datetime
from pathlib import Path
import sys

INPUT_CSV = "ywh_v4_videos_2025.csv"
OUTPUT_CSV = "ywh_v5_datetime.csv"


def iso_to_mysql(ts):
    """
    Convert ISO-8601 timestamp to MySQL DATETIME format.
    """
    if not ts:
        return ""

    try:
        # Handle milliseconds + Z
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""


def main():
    input_path = Path(INPUT_CSV)

    if not input_path.exists():
        print("Input CSV not found")
        sys.exit(1)

    with open(input_path, newline="", encoding="utf-8") as fin, \
         open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fout:

        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            row["watched_at"] = iso_to_mysql(row.get("watched_at"))
            row["published_at"] = iso_to_mysql(row.get("published_at"))
            writer.writerow(row)

    print(f"Converted CSV written to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
