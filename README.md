# YooTube_Watch-history_Analysis
Analyze and visualize Youtube watch history

I cleaned, enriched, and anonymized my personal YouTube watch history from two accounts (Main and Educational) to tell a data story for 2025. The workflow turns raw Google Takeout exports into analysis-ready, anonymized tables and activity scores.

## Data Sources

- Google Takeout watch history exports for each account
- YouTube Data API v3 to enrich with titles, channels, durations, categories, views, and likes

## How I Processed the Data

1. **Collect**: Parsed the raw Takeout JSON and pulled full metadata for every video via the YouTube Data API, caching responses to avoid redundant calls.
2. **Combine**: Built per-account tables, tagged each row by account, and merged both histories into one timeline.
3. **Clean & Filter**: Standardized timestamps, removed livestreams and outliers, and focused the analysis on 2025 watches.
4. **Normalize Time**: Converted ISO timestamps to SQL-friendly datetimes and floored them to the nearest hour for consistent aggregation.
5. **Anonymize**: Replaced video identifiers and URLs with generated IDs, dropped sensitive fields, and masked non-top channels while keeping the highest-impact channels intact.
6. **Validate Quality**: Excluded rows without reliable channel or duration info (e.g., removed/private videos) to prevent skew.
7. **Enrich for Analysis**: Added local hour buckets, day-of-week labels, and harmonized content types (short vs. long form).
8. **Score Activity**: Computed daily watch hours and frequency, then built a weighted activity score (70% hours, 30% frequency) with percentile caps to tame extreme sessions.

## What You Get

- An anonymized, analysis-ready 2025 watch history with clean time features and content labels
- Daily activity scores and levels across the full year
- Intermediate checkpoints that show each transformation stage for transparency

## Quickstart (rerun or adapt)

1. **Set up environment**: Create/activate a Python env (e.g., the `analytics` conda env) and install pandas, requests, python-dotenv, matplotlib, and calplot.
2. **Add your API key**: Create a `.env` file with `YT_API=your_youtube_api_key` (YouTube Data API v3).
3. **Drop in raw data**: Place your Google Takeout `watch-history.json` files for each account into the working directory.
4. **Fetch metadata**: Run the metadata fetch step to pull titles, channels, durations, categories, views, and likes for every video ID (responses are cached to avoid repeat calls).
5. **Build the dataset**: Generate a table per account (if you have multiple accounts, tag and merge them; if not, proceed with your single account), deduplicate non-music titles, and remove livestreams/outliers; keep only the target year (2025 in this project).
6. **Normalize and anonymize**: Convert timestamps to SQL-friendly datetimes, floor to the hour, replace video identifiers with generated IDs, and mask non-top channels.
7. **Finalize and score**: Add local hour/day-of-week features, drop rows without reliable duration/channel info, and compute daily watch hours, frequencies, and a percentile-capped activity score.
8. **Inspect outputs**: Use the final anonymized table and the daily activity-score table for analysis or visualization; intermediate checkpoints remain available for traceability.

## Methodological Notes

- Removed/private videos (~4–26% of events) are excluded because they lack the fields needed for fair analysis.
- YouTube watch history records only video start times, as this is the only data YouTube provides. Additionally, I often download long videos for offline viewing using external tools, which helps reduce the upward bias caused by missing watch-duration data.
