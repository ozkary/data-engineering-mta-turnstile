{{ config(materialized='table') }}

select 
    booth_id,
    "remote",
    booth_name
from {{ ref('stg_booth') }}