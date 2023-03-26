### Create an external table by linking it to blob storage files

CREATE OR REPLACE EXTERNAL TABLE mta_data.ext_turnstile
OPTIONS (
  format = 'parquet',
  uris = ['gs://ozkary_data_lake_ozkary-de-101/turnstile/*.parquet']  
);