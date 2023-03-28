{{ config(materialized='view') }}

with turnstile as 
(
  select     
  CA,
  UNIT,
  STATION,
  concat(CA,UNIT,SCP) as REF,
  SCP,
  LINENAME,
  DIVISION,
  concat(log.DATE," ", log.TIME) as CREATED,
  ENTRIES,
  EXITS,
    row_number() over(partition by CA, UNIT, SCP) as rn
  from {{ source('staging','ext_turnstile') }} as log
  
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['REF', 'CREATED']) }} as log_id,
    CA as booth,
    UNIT as remote,
    STATION as station,

    -- unit and line information
    SCP as scp,
    LINENAME AS line_name,
    DIVISION AS division,

     -- timestamp
    cast(CREATED as timestamp) as created_dt,    
       
    -- measures
    cast(entries as integer) as entries,
    cast(exits as integer) as exits    
from turnstile
where rn = 1


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}