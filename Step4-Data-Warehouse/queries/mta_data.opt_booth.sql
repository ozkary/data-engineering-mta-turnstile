CREATE OR REPLACE TABLE `ozkary-de-101`.`mta_data`.opt_booth
CLUSTER BY booth_id  -- BigQuery will physically sort data blocks based on this key
AS
SELECT
  booth_id,
  remote,
  booth_name,
  station_name
FROM
  `ozkary-de-101`.`mta_data`.vw_booth
;