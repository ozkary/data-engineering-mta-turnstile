CREATE OR REPLACE VIEW mta_data.vw_date AS
WITH
-- 1. Generate all dates from 2020-01-01 through 2035-01-01
generate_dates AS (
  SELECT
    full_date
  FROM
    UNNEST(
      GENERATE_DATE_ARRAY(DATE('2020-01-01'), DATE('2035-01-01'), INTERVAL 1 DAY)
    ) AS full_date
)

-- 2. Select the dates and derive time attributes
SELECT
  -- Create a unique, deterministic ID (date_id) for the date.
  -- Simplified key generation since full_date is always non-null here.
  TO_HEX(MD5(CAST(t.full_date AS STRING))) AS date_id,

  t.full_date AS date_key,

  -- Calendar Attributes
  EXTRACT(YEAR FROM t.full_date) AS year_number,
  EXTRACT(QUARTER FROM t.full_date) AS quarter_number,
  EXTRACT(MONTH FROM t.full_date) AS month_number,
  FORMAT_DATE('%B', t.full_date) AS month_name,
  FORMAT_DATE('%b', t.full_date) AS month_name_short,
  EXTRACT(DAY FROM t.full_date) AS day_of_month,

  -- Day of Week Attributes
  EXTRACT(DAYOFWEEK FROM t.full_date) AS day_of_week_number, -- 1=Sunday, 7=Saturday
  FORMAT_DATE('%A', t.full_date) AS day_of_week_name,
  FORMAT_DATE('%a', t.full_date) AS day_of_week_name_short,

  -- Flags
  CASE
    -- BigQuery DAYOFWEEK: 1=Sunday, 7=Saturday
    WHEN EXTRACT(DAYOFWEEK FROM t.full_date) IN (1, 7) THEN TRUE
    ELSE FALSE
  END AS is_weekend

FROM
  generate_dates AS t;