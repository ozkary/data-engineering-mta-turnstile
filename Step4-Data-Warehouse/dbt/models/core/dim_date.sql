{{ config(materialized='table',
  partition_by={
    "field": "full_date",
    "data_type": "date",
    "granularity": "year"
  }) 
}}

-- Specify that this model references the stg_dim_date view
select
  date_id,
  full_date,
  year,
  quarter,
  month,
  month_name,
  day,
  day_of_week,
  day_of_week_name,
  is_weekend,
  -- is_holiday,  -- Optional
  -- fiscal_year,  -- Optional
  -- fiscal_quarter  -- Optional
from {{ ref('stg_date') }}
