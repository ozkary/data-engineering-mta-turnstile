{{ config(materialized='view') }}

with turnstile as 
(
  select   
  concat(log."C/A",UNIT) as BOOTH
  STATION,
  concat(log."C/A",UNIT,SCP) as REF
  SCP,
  LINENAME,
  DIVISION,
  CREATED = concat(log.DATE," ", log.TIME) 
  ENTRIES,
  EXITS,
    row_number() over(partition by log."C/A", UNIT, SCP) as rn
  from {{ source('staging','ext_turnstile') }} as log
  
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['REF', 'CREATED']) }} as log_id,
    BOOTH as booth,
    STATION as station,

    -- unit and line information
    SCP as scp,
    LINENAME AS line_name,
    DIVISION AS division,

     -- timestamp
    cast(CREATED as timestamp) as created_dt,    
       
    -- measures
    cast(entries as integer) as entries
    cast(exits as integer) as exits    
from turnstile
where rn = 1


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}