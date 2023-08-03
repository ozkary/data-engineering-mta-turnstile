{{ config(materialized='view') }}

with booths as 
(
  select
    UNIT,
    CA,
    Station,
    row_number() over(partition by UNIT, CA) as rn
  from {{ source('staging','ext_turnstile') }}   
  where Unit is not null and CA is not null and Station is not null
)
select
    -- create a unique key 
    {{ dbt_utils.generate_surrogate_key(['UNIT', 'CA']) }} as booth_id,
    UNIT as remote,
    CA as booth_name,
    Station as station_name
from booths
where rn = 1

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}