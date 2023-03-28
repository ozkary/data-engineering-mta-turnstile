{{ config(materialized='view') }}

with stations as 
(
  select 
    Station,
    row_number() over(partition by Station) as rn
  from {{ source('staging','remote_booth_station') }}   
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['Station']) }} as station_id,    
    Station as station_name
from stations
where rn = 1

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}