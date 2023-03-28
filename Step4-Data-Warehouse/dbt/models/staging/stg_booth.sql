{{ config(materialized='view') }}

with booths as 
(
  select
    Remote,
    Booth,
    Station,
    row_number() over(partition by Remote, Booth) as rn
  from {{ source('staging','remote_booth_station') }}   
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['Remote', 'Booth']) }} as booth_id,
    Remote as remote,
    Booth as booth_name,
    Station as station_name
from booths
where rn = 1

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}