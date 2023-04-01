{{ config(materialized='incremental') }}

with stations as (
select 
    station_id, 
    station_name    
from mta_data.stg_turnstile as d
)
select
    ns.station_id,
    ns.station_name
from stations ns
     -- logic for incremental models this = dim_station table
    left outer join mta_data.dim_station dim
        on ns.station_id = dim.station_id
    where dim.station_id is null      



