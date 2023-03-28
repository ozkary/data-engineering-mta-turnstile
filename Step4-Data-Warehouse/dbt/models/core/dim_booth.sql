{{ config(materialized='table',
   cluster_by = "station_id"
 )}}

with booth as (
select 
    booth_id,
    remote,
    booth_name,
    station_name
from {{ ref('stg_booth') }}
),

dim_station as (
    select station_id, station_name from {{ ref('dim_station') }}   
)
select 
    booth_id,
    remote,
    booth_name,
    station_id
from booth b 
inner join dim_station s 
    on b.station_name = s.station_name

