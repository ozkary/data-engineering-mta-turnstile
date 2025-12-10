CREATE OR REPLACE VIEW mta_data.vw_station AS
WITH
-- 1. Deduplicate the source data to get one unique record per Station Name
deduplicated_stations AS (
  SELECT
    t.Station,
    -- Assign a row number based on the unique key (Station)
    -- We will select rn = 1 to ensure uniqueness
    ROW_NUMBER() OVER(PARTITION BY t.Station) AS rn
  FROM
    `mta_data.vw_ext_turnstile` AS t
  WHERE
    -- Filter out any records where Station name might be missing (though often not strictly necessary for this file)
    t.Station IS NOT NULL
)

-- 2. Select the unique station records and create the surrogate key
SELECT
  -- Create a unique, deterministic ID for the station using a hash function.
  -- The original dbt-style key is simplified since we filtered for non-null Stations.
  TO_HEX(MD5(t.Station)) AS station_id,

  -- Renaming and standardizing the station name column.
  t.Station AS station_name

FROM
  deduplicated_stations AS t

WHERE
  -- Select only the first record from the partition to enforce uniqueness (deduplication)
  t.rn = 1
;