CREATE TABLE mta_data.fact_stats (
  name STRING,
  total INT64,
  created DATETIME DEFAULT CURRENT_DATETIME()
);
