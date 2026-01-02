"""
Use youtube data API v3 to get metadata for the videos in watdh history
"""

from pathlib import Path
from datetime import datetime, timezone
import os
import re
import json
import sys
import requests
from dotenv import load_dotenv


CACHE_FILE = "youtube_video_cache_full_2.json"

load_dotenv()
API_KEY = os.getenv("YT_API")

if not API_KEY:
    raise RuntimeError("YT_API not found in .env file")

def iso8601_to_seconds(duration):
    """
    Convert ISO 8601 YouTube duration
    """
    if not duration or "D" in duration:
        return None

    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not match:
        return None

    h = int(match.group(1) or 0)
    m = int(match.group(2) or 0)
    s = int(match.group(3) or 0)

    return h * 3600 + m * 60 + s

def load_cache():
    if Path(CACHE_FILE).exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return {v["video_id"]: v for v in json.load(f)}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(cache.values()), f, indent=2)

# ------------------ API FETCH ------------------

def fetch_metadata(video_ids):
    results = {}
    batch = []

    def query(ids):
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "id": ",".join(ids),
            "key": API_KEY,
            "part": "snippet,contentDetails,statistics,topicDetails"
        }

        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()

        for item in r.json().get("items", []):
            results[item["id"]] = {
                "video_id": item["id"],
                "fetched_at": datetime.now(timezone.utc).isoformat(),

                "snippet": {
                    "title": item["snippet"]["title"],
                    "channelTitle": item["snippet"]["channelTitle"],
                    "publishedAt": item["snippet"]["publishedAt"],
                    "categoryId": item["snippet"]["categoryId"]
                },

                "contentDetails": {
                    "duration_seconds": iso8601_to_seconds(
                        item["contentDetails"]["duration"]
                    ),
                    "definition": item["contentDetails"].get("definition"),
                    "caption": item["contentDetails"].get("caption")
                },

                "statistics": {
                    "viewCount": int(item["statistics"].get("viewCount", 0)),
                    "likeCount": int(item["statistics"].get("likeCount", 0))
                },

                "topicDetails": item.get("topicDetails", {})
            }

    for vid in video_ids:
        batch.append(vid)
        if len(batch) == 50:
            query(batch)
            batch.clear()

    if batch:
        query(batch)

    return results

# ------------------ MAIN ------------------

if len(sys.argv) < 2:
    print("Usage: python yt_cache_full_metadata.py watch-history.json")
    sys.exit(1)

WATCH_FILE = sys.argv[1]

with open(WATCH_FILE, "r", encoding="utf-8") as f:
    history = json.load(f)

video_ids = {
    e["titleUrl"]
    .replace("\\u003d", "=")
    .split("watch?v=")[1]
    .split("&")[0]
    for e in history
    if "titleUrl" in e and "watch?v=" in e["titleUrl"]
}

cache = load_cache()
missing = [vid for vid in video_ids if vid not in cache]

print(f"Total unique videos: {len(video_ids)}")
print(f"Already cached: {len(cache)}")
print(f"Fetching now: {len(missing)}")

if missing:
    fetched = fetch_metadata(missing)
    cache.update(fetched)
    save_cache(cache)

print("Full metadata cache saved → youtube_video_cache_full.json")
