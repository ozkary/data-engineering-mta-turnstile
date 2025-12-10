CREATE MATERIALIZED VIEW `ozkary-de-101`.`mta_data`.mv_turnstile
OPTIONS (
  enable_refresh = FALSE  -- Prevents automatic refreshing to control costs
  -- refresh_interval_minutes = 60
)
AS
SELECT
  log_id,
  booth_ca,
  turnstile_unit,
  station_name,
  turnstile_scp,
  line_name,
  division,
  created_dt,
  entries,
  exits
FROM
  `ozkary-de-101`.`mta_data`.vw_turnstile
;