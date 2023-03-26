{{ config(materialized='view') }}

with booth as 
(
  select
    "Remote",
    Booth,
    row_number() over(partition by "Remote", Booth) as rn
  from {{ source('staging','remote_booth_station') }}   
)
select
    -- identifiers
    rn as booth_id,
    "Remote" as "remote",
    Booth as booth_name
from booth
where rn = 1

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}