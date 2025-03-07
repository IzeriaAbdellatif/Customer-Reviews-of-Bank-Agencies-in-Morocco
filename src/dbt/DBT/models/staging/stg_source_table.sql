with source_data as (
    select * from {{ source('db1', 'banks') }}
)
select * from source_data
