{{ config(materialized='incremental') }}

with stations as (
select 
    station_id, 
    station_name    
from {{ ref('stg_station') }} as d
where station_id is not null
)
select
    ns.station_id,
    ns.station_name
from stations ns
{% if is_incremental() %}
     -- logic for incremental models this = dim_station table
    left outer join {{ this }} dim
        on ns.station_id = dim.station_id
    where dim.station_id is null     

 {% endif %}



