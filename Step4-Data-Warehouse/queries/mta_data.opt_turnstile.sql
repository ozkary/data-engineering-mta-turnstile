-- DROP TABLE `ozkary-de-101`.`mta_data`.opt_turnstile
CREATE OR REPLACE TABLE `ozkary-de-101`.`mta_data`.opt_turnstile
PARTITION BY DATE(created_dt) -- 1. Partition by the date column to reduce data scanned based on time ranges
CLUSTER BY station, booth -- 2. Cluster by foreign keys for efficient joining
AS
SELECT
  log_id,
  booth,
  remote,
  station,
  scp,
  line_name,
  division,
  created_dt,
  entries,
  exits
FROM
  `ozkary-de-101`.`mta_data`.vw_turnstile
;