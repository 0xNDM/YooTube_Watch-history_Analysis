"""
Merge corresponding data from watch history and youtube video cache jsons for each account to a csv file
"""

import json
import csv

# Input files
WATCH_FILE = "watch-history.json"
CACHE_FILE = "youtube_video_cache_full.json"
OUTPUT_CSV = "youtube_history.csv"

# Category mapping
CATEGORY_MAP = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "19": "Travel & Events",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
    "30": "Movies",
    "31": "Anime/Animation",
    "32": "Action/Adventure",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers"
}

with open(WATCH_FILE, "r", encoding="utf-8") as f:
    watch_history = json.load(f)

with open(CACHE_FILE, "r", encoding="utf-8") as f:
    cache_list = json.load(f)

cache_by_id = {v["video_id"]: v for v in cache_list}

merged_rows = []

for entry in watch_history:
    if "titleUrl" not in entry or "watch?v=" not in entry["titleUrl"]:
        continue

    # Extract video_id
    video_id = (
        entry["titleUrl"]
        .replace("\\u003d", "=")
        .split("watch?v=")[1]
        .split("&")[0]
    )

    watched_at = entry.get("time")
    video_meta = cache_by_id.get(video_id)

    duration_seconds = (
        video_meta["contentDetails"]["duration_seconds"]
        if video_meta and video_meta.get("contentDetails") else None
    )

    # Determine type
    video_type = "short" if duration_seconds and duration_seconds <= 90 else "video"

    # Map category
    category_id = (
        video_meta["snippet"]["categoryId"]
        if video_meta and video_meta.get("snippet") else None
    )
    category_name = CATEGORY_MAP.get(category_id, "Unknown") if category_id else None

    # Channel from cache if available
    channel_title = (
        video_meta["snippet"]["channelTitle"]
        if video_meta and video_meta.get("snippet") else None
    )

    merged_rows.append({
        "Title": video_meta["snippet"]["title"] if video_meta and video_meta.get("snippet") else entry.get("title"),
        "Channel": channel_title,
        "watched_at": watched_at,
        "published_at": video_meta["snippet"]["publishedAt"] if video_meta and video_meta.get("snippet") else None,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "video_id": video_id,
        "categoryId": category_id,
        "category": category_name,
        "duration_seconds": duration_seconds,
        "views": video_meta["statistics"]["viewCount"] if video_meta and video_meta.get("statistics") else None,
        "likes": video_meta["statistics"]["likeCount"] if video_meta and video_meta.get("statistics") else None,
        "type": video_type
    })

# Write CSV
fieldnames = [
    "Title", "Channel", "watched_at", "published_at", "url",
    "video_id", "categoryId", "category",
    "duration_seconds", "views", "likes", "type"
]

with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in merged_rows:
        writer.writerow(row)

print(f"Saved {len(merged_rows)} rows → {OUTPUT_CSV}")
