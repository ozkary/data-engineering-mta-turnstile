-- check station dimension table
select count(*) from mta_data.dim_station;

-- check booth dimension table
select count(*) from mta_data.dim_booth;

-- check the fact table
select count(*) from mta_data.fact_turnstile;

-- check the staging fact data
select count(*) from mta_data.stg_turnstile;


-- check the external table (Data Lake)