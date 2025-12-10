CREATE OR REPLACE EXTERNAL TABLE `ozkary-de-101`.`mta_data`.`ext_turnstile`( 
  int64_field_0 INT64,
  CA STRING,
  UNIT STRING,
  SCP STRING,
  STATION STRING,
  LINENAME STRING,
  DIVISION STRING,
  DATE DATE,
  TIME TIME,
  DESC STRING,
  ENTRIES INT64,
  EXITS INT64
) 
OPTIONS ( 
  format = 'CSV',
  uris = ['gs://your-bucket/your-path/ext_turnstile.csv'],
  skip_leading_rows = 1,    
  compression = 'GZIP'
);