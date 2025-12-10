-- DROP TABLE `ozkary-de-101`.`mta_data`.opt_station
CREATE OR REPLACE TABLE `ozkary-de-101`.`mta_data`.opt_station
CLUSTER BY station_id  -- BigQuery will physically sort data blocks based on this key
AS
SELECT
  station_id,
  station_name
FROM
  `ozkary-de-101`.`mta_data`.vw_station
;