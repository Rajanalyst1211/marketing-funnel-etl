with source as (

    select * from {{ source('main', 'raw_leads') }}

),

cleaned as (

    select
        lead_id,
        date(created_date)              as lead_date,
        lower(trim(source_channel))     as channel,
        lower(trim(industry))           as industry,
        trim(region)                    as region,
        trim(stage)                     as stage,
        coalesce(revenue, 0.0)          as revenue,
        trim(sales_rep)                 as sales_rep,
        trim(company_name)              as company_name

    from source

    where lead_id is not null
      and stage is not null

)

select * from cleaned
