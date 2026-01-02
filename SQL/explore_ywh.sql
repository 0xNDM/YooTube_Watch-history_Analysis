SELECT account, COUNT(*) AS videos
FROM ywh
GROUP BY account;

select count (distinct title)
from ywh;

SELECT
  ROUND(SUM(duration_seconds) / 3600, 2) AS total_watch_hours
FROM ywh
WHERE duration_seconds IS NOT NULL;


select type,
  ROUND(SUM(duration_seconds) / 3600, 2) AS total_watch_hours
FROM yt.ywh
where watched_at between "2024-01-01" and "2025-01-01"
group by type;

select category ,
  count(*),
  ROUND(SUM(duration_seconds) / 3600, 2) AS hours
FROM yt.ywh
where watched_at >= "2025-01-01" and type = "video"
group by category 
order by hours desc;

SELECT
  DATE(watched_at) AS day,
  ROUND(SUM(duration_seconds) / 3600, 2) AS hours,
  count(*) as times
FROM ywh_v7_anonymized
GROUP BY day
ORDER BY times desc ;

SELECT
  HOUR(watched_at) AS hour,
  COUNT(*) AS videos
FROM ywh
GROUP BY hour
ORDER BY hour;

SELECT
  YEAR(watched_at) AS year,
  MONTH(watched_at) AS month,
  COUNT(*) AS videos
FROM ywh
GROUP BY year, month
ORDER BY year, month;

SELECT
  Channel,
  COUNT(*) AS times,
  ROUND(SUM(duration_seconds) / 3600, 2) AS hours
FROM ywh
where year(watched_at) =2025
GROUP BY Channel
ORDER BY times DESC
LIMIT 20;

select title, duration_seconds
from ywh
order by duration_seconds desc;

select category,
  ROUND(AVG(views)) AS avg_views
FROM ywh
WHERE views IS NOT NULL
group by category;

select title, views
from ywh
where category = "Education" and type = "video"
order by views desc;

SELECT
  CASE
    WHEN views < 10000 THEN 'Very niche'
    WHEN views < 200000 THEN 'Niche'
    WHEN views < 2000000 THEN 'Popular'
    ELSE 'Very popular'
  END AS popularity,
  COUNT(*) AS videos
FROM ywh
WHERE views IS NOT NULL
GROUP BY popularity;

SELECT
  ROUND(avg(duration_seconds) ) AS shorts_hours
FROM ywh
WHERE type = 'video';

SELECT
  ROUND(
    SUM(type = 'short') / COUNT(*) * 100, 2
  ) AS shorts_percentage
FROM ywh;

SELECT
  ROUND(AVG(DATEDIFF(watched_at, published_at)), 1) AS avg_days_after_publish
FROM ywh
WHERE published_at IS NOT null and category = "news & politics";

SELECT
  DATE(watched_at) AS day,
  ROUND(
    SUM(SUM(duration_seconds)) OVER (
      ORDER BY DATE(watched_at)
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) / 3600, 2
  ) AS rolling_7d_hours
FROM ywh
GROUP BY day
ORDER BY day;

SELECT
  COUNT(*) AS total,
  SUM(duration_seconds > 3*3600) AS over_3h,
  SUM(duration_seconds > 6*3600) AS over_6h,
  SUM(duration_seconds > 12*3600) AS over_12h,
  SUM(duration_seconds > 20*3600) AS over_20h
FROM ywh;

select 
	YEAR(watched_at) AS year,
	MONTH(watched_at) AS month,
	COUNT(*) AS videos
from ywh
where 
	duration_seconds is null and
	year(watched_at) = 2025
group by year, month 
order by year, month;

-- Distinct values
SELECT COUNT(DISTINCT video_id) from ywh where category != "music";

SELECT title, COUNT(*) AS repetition_count
FROM ywh
GROUP BY title
ORDER BY repetition_count DESC;

SELECT COUNT(title) 
from ywh
where category != "music" and YEAR(watched_at) = 2025;

-- check for a string using regexp
select *
from ywh 
-- where lower(title) like "%lyrics%" and category != "Music";
where title regexp "lyrics|music|song|mezmur" 
	and category != "Music"
	and type = "video"
	and duration_seconds < 400;

-- week by week 
SELECT
    YEAR(watched_at)            AS year,
    WEEK(watched_at, 3)         AS week,
    round(sum(duration_seconds) / 3600, 2) as total
FROM ywh
WHERE watched_at IS NOT null and year(watched_at) =2025
GROUP BY
    YEAR(watched_at),
    WEEK(watched_at, 3)
ORDER BY
  total DESC;

select title, duration_seconds, channel
from ywh_v3_livestream_removed
where duration_seconds > 6000
	and year(watched_at) = 2025
	and lower(channel) not regexp "podcast|good"
order by duration_seconds desc;

-- Sub query and using having instead of where for aggregated results
select count(*) as no_of_channels
from (
	select channel, count(*) as n, ROUND(SUM(duration_seconds) /3600  , 2) AS hours
	from ywh_v4_removed_videos
	where type = "video"
	group by channel
	having n < 2
	order by  n
) sub; -- sub can be whatever I like it refers to the inner/sub query

