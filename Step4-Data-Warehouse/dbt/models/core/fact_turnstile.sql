{{ config(materialized='table',
    partition_by={
      "field": "created_dt",
      "data_type": "timestamp",
      "granularity": "day"},
      cluster_by = "station_id",
) }}

with turnstile as (
    select 
        log_id,
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
)

dim_booth as (
    select booth_id, "remote", booth_name  from {{ ref('dim_zones') }}   
)
select 
    log_id,
    station_id,
    booth_id,
    scp,
    line_name,
    division,
    created_dt,
    entries,
    exits
from turnstile log
left join dim_station as station
   on log.station = station.station_name
left join dim_booth as booth
on log.booth = concat(booth."remote",booth.booth_name)