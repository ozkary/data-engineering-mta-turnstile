CREATE OR REPLACE VIEW mta_data.vw_booth AS
WITH
-- 1. Deduplicate the source data to get one unique record per Booth (UNIT + CA)
deduplicated_booths AS (
  SELECT
    t.UNIT,
    t.CA,
    t.Station,
    -- Assign a row number based on the unique key (UNIT, CA)
    -- We will select rn = 1 to ensure a 1:1 relationship between UNIT/CA and Station
    ROW_NUMBER() OVER(PARTITION BY t.UNIT, t.CA) AS rn
  FROM
    `ozkary-de-101.mta_data.vw_ext_turnstile` AS t
  WHERE
    t.UNIT IS NOT NULL
    AND t.CA IS NOT NULL
    AND t.Station IS NOT NULL
)

-- 2. Select the unique booth records and create the surrogate key
SELECT
  -- Create a unique, deterministic ID for the booth using a hash function.
  -- This replaces the original complex dbt-style surrogate key implementation.
  TO_HEX(MD5(CONCAT(t.UNIT, '_', t.CA))) AS booth_id,

  -- Renaming and standardizing columns for clarity and consistency.
  t.UNIT AS remote,       -- Unique identifier for the turnstile assembly unit
  t.CA AS booth_name,     -- Control Area identifier (e.g., Booth ID/Code)
  t.Station AS station_name       -- Name of the station where the booth is located

FROM
  deduplicated_booths AS t

WHERE
  -- Select only the first record from the partition to enforce uniqueness (deduplication)
  t.rn = 1
;