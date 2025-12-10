CREATE OR REPLACE VIEW mta_data.vw_turnstile AS
WITH
-- Deduplicate source records to ensure a unique entry for each time/location stamp.
deduplicated_logs AS (
  SELECT
    t.CA,
    t.UNIT,
    t.STATION,
    t.SCP,
    t.LINENAME,
    t.DIVISION,
    -- Concatenate DATE and TIME strings for later timestamp conversion
    CONCAT(t.DATE, ' ', t.TIME) AS created_ts_str,
    t.ENTRIES,
    t.EXITS,
    -- Assign a row number to deduplicate based on time and location
    ROW_NUMBER() OVER(PARTITION BY t.CA, t.UNIT, t.SCP, t.DATE, t.TIME) AS rn
  FROM
    `ozkary-de-101`.`mta_data`.`vw_ext_turnstile` AS t
)

-- Select the unique records, apply transformations, and create the final fact table structure.
SELECT
  -- Create a unique, deterministic ID (log_id) for the row based on the unique time/location.
  TO_HEX(MD5(CONCAT(t.CA, t.UNIT, t.SCP, '_', t.created_ts_str))) AS log_id,

  -- Identifiers for joining to dimension tables
  t.CA AS booth,           -- Booth Control Area
  t.UNIT AS remote,   -- Turnstile assembly unit ID
  t.STATION AS station,  -- Station name

  -- Unit and line information
  t.SCP AS scp,     -- Specific turnstile position
  t.LINENAME AS line_name,    -- Line name
  t.DIVISION AS division,     -- MTA Division

  -- Timestamp
  -- Cast the concatenated DATE and TIME string into a TIMESTAMP type
  CAST(t.created_ts_str AS TIMESTAMP) AS created_dt,

  -- Measures (cast to the correct numeric type)
  CAST(t.ENTRIES AS INT64) AS entries,
  CAST(t.EXITS AS INT64) AS exits

FROM
  deduplicated_logs AS t

WHERE
  -- Select only the first record from the partition to enforce uniqueness
  t.rn = 1
;