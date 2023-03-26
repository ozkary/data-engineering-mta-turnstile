{{ config(materialized='table') }}

select 
    station_id, 
    station_name    
from {{ ref('stg_station') }}