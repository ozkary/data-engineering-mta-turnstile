{{ config(materialized='view') }}

with log as 
(
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
  from {{ ref('fact_turnstile') }}   
),

stations as (

    select 
        station_id,
        station_name
    from {{ ref('dim_station') }}   
),

booths as (

    select 
        booth_id,
        booth_name
    from {{ ref('dim_booth') }}   
)

select  
    l.log_id,  
    s.station_name,
    b.booth_name,
    l.scp,
    l.line_name,
    l.division,
    l.created_dt,
    l.entries,
    l.exits,
    CURRENT_DATE() as reported_dt
from log as l
inner join stations as s on l.station_id = s.station_id
inner join booths as b on l.booth_id = b.booth_id
where created_dt > '2023-01-01'

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}