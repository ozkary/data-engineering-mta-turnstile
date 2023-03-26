{{ config(materialized='view') }}

with booth as 
(
  select 
    Station,
    row_number() over(partition by Station) as rn
  from {{ source('staging','remote_booth_station') }}   
)
select
    -- identifiers
    rn as station_id,
    Station as station_name
from booth
where rn = 1

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}