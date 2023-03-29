{{ config(materialized='incremental',
   cluster_by = "station_id"
 )}}

with booth as (
select 
    booth_id,
    remote,
    booth_name,
    station_name
from {{ ref('stg_booth') }}
),

dim_station as (
    select station_id, station_name from {{ ref('dim_station') }}   
)
select 
    b.booth_id,
    b.remote,
    b.booth_name,
    st.station_id
from booth b 
inner join dim_station st 
    on b.station_name = st.station_name
{% if is_incremental() %}
     -- logic for incremental models this = dim_booth table
    left outer join {{ this }} s
        on b.booth_id = s.booth_id
    where s.booth_id is null     
 {% endif %}


