with leads as (

    select * from {{ ref('stg_leads') }}

),

funnel as (

    select
        channel,
        count(*)                                         as total_leads,

        sum(case when stage = 'MQL'
            then 1 else 0 end)                           as total_mqls,

        sum(case when stage = 'SQL'
            then 1 else 0 end)                           as total_sqls,

        sum(case when stage = 'Opportunity'
            then 1 else 0 end)                           as total_opportunities,

        sum(case when stage = 'Customer'
            then 1 else 0 end)                           as total_customers,

        round(sum(revenue), 2)                           as total_revenue

    from leads
    group by channel

)

select
    channel,
    total_leads,
    total_mqls,
    total_sqls,
    total_opportunities,
    total_customers,
    total_revenue,

    round(
        100.0 * total_customers / nullif(total_leads, 0)
    , 2)                                                 as lead_to_customer_pct,

    round(
        total_revenue / nullif(total_customers, 0)
    , 2)                                                 as avg_deal_size_usd

from funnel
order by total_revenue desc