CREATE TABLE `mta.fact_turnstile` (
  log_id INT64 PRIMARY KEY,
  station_id INT64 REFERENCES `mta.dim_station`(station_id),
  booth_id INT64 REFERENCES `mta.dim_booth`(booth_id),
  scp STRING,
  line_name STRING,
  division STRING,
  created_dt TIMESTAMP,
  entries INT64,
  exits INT64
)
PARTITION BY DATE(created_dt);  -- Daily partitioning
CLUSTER BY station_id;
