{{ config(materialized='view') }}

with turnstile as (
    select 
        log_id,
        remote,
        booth,
        station,
        scp,
        line_name,
        division,
        created_dt,
        entries,
        exits    
    from {{ ref('stg_turnstile') }}   
), 

dim_station as (
    select station_id, station_name from {{ ref('dim_station') }}   
),

dim_booth as (
    select booth_id, remote, booth_name  from {{ ref('dim_booth') }}   
)
select 
    log.log_id,
    st.station_id,
    booth.booth_id,
    log.scp,
    log.line_name,
    log.division,
    log.created_dt,
    log.entries,
    log.exits
from turnstile as log
left join dim_station as st
   on log.station = st.station_name
left join dim_booth as booth
on log.remote = booth.remote and log.booth = booth.booth_name      
    left outer join mta_data.fact_turnstile fact
        on log.log_id = fact.log_id
    where fact.log_id is null     