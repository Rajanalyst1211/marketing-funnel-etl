with source as (

    select * from {{ source('main', 'raw_campaign_spend') }}

),

cleaned as (

    select
        trim(month)                     as month,
        lower(trim(channel))            as channel,
        coalesce(spend_usd, 0.0)        as spend_usd

    from source

    where month   is not null
      and channel is not null

)

select * from cleaned