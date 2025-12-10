CREATE MATERIALIZED VIEW `ozkary-de-101`.`mta_data`.mv_booth
OPTIONS (
  enable_refresh = FALSE  -- Prevents automatic refreshing to control costs
  -- refresh_interval_minutes = 1440
)
AS
SELECT
  booth_id,
  remote,
  booth_name,
  station_name
FROM
  `ozkary-de-101`.`mta_data`.vw_booth
;