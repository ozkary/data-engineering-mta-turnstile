-- This SQL file defines a view (stg_date) for initial data population
{{ config(materialized='view') }}

with generate_dates as 
(
   SELECT full_date
    FROM UNNEST(
        GENERATE_DATE_ARRAY(DATE('2020-01-01'), DATE('2035-01-01'), INTERVAL 1 DAY)      
    ) as full_date
)
select    
  {{ dbt_utils.generate_surrogate_key(['full_date']) }} as date_id,  
  full_date,
  EXTRACT(YEAR FROM full_date) as year,
  EXTRACT(QUARTER FROM full_date) AS quarter,
  EXTRACT(MONTH FROM full_date) as month,
  FORMAT_DATE('%b', full_date) as month_name,  -- Adjust based on your database dialect
  EXTRACT(DAY FROM full_date) as day,
  EXTRACT(DAYOFWEEK FROM full_date) as day_of_week,
  FORMAT_DATE('%a', full_date) as day_of_week_name,  -- Adjust based on your database dialect
  case when EXTRACT(DAYOFWEEK from full_date) in (1, 7) then TRUE ELSE FALSE END AS is_weekend

  -- is_holiday, --Add logic to populate is_holiday (optional)
  -- fiscal_year,  -- Optional, replace with your logic if applicable
  -- fiscal_quarter  -- Optional, replace with your logic if applicable
from generate_dates
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}