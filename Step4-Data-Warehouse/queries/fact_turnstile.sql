-- select count(*) from mta_data.dim_station;
-- select count(*) from mta_data.dim_booth;

-- get the date range 
select min(created_dt) as start_update,  max(created_dt) as end_update from mta_data.fact_turnstile limit 100;

-- select count(*) from mta_data.fact_turnstile;
-- select count(*) from mta_data.stg_turnstile;
-- select count(*) from mta_data.ext_turnstile;


insert into mta_data.fact_stats (name, total)

select 'dim_station' as name, count(*) as total from mta_data.dim_station
union all
select 'dim_booth', count(*) from mta_data.dim_booth
union all 
select 'fact_turnstile', count(*) from mta_data.fact_turnstile


select * from mta_data.fact_stats