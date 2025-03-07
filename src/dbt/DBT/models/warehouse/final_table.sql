{{ config(
    materialized='table',
    schema='public',
    database='db2'
) }}

select * from {{ ref('stg_source_table') }}
