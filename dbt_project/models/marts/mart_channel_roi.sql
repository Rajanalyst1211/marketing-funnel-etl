with funnel as (

    select * from {{ ref('mart_funnel_metrics') }}

),

spend as (

    select
        channel,
        round(sum(spend_usd), 2) as total_spend_usd
    from {{ ref('stg_campaign_spend') }}
    group by channel

),

joined as (

    select
        f.channel,
        f.total_leads,
        f.total_customers,
        f.total_revenue,
        s.total_spend_usd,

        round(
            s.total_spend_usd / nullif(f.total_leads, 0)
        , 2)                                             as cost_per_lead_usd,

        round(
            s.total_spend_usd / nullif(f.total_customers, 0)
        , 2)                                             as cost_per_customer_usd,

        round(
            f.total_revenue / nullif(s.total_spend_usd, 0)
        , 2)                                             as roas

    from funnel f
    left join spend s on lower(f.channel) = lower(s.channel)

)

select * from joined
order by roas desc