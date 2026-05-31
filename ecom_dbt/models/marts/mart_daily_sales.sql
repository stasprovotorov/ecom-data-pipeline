with orders_daily as (
    select
        order_date::date as order_date,
        count(order_id) as orders_count,
        count(distinct user_id) as buyers_count,
        round(coalesce(sum(total_amount), 0), 2) as total_amount
    from {{ ref('stg_orders') }}
    group by order_date::date
),
items_daily as (
    select
        o.order_date::date as order_date,
        coalesce(sum(i.quantity), 0) as items_sold
    from {{ ref('stg_order_items') }} as i
    left join {{ ref('stg_orders') }} as o
        on i.order_id = o.order_id
    group by o.order_date::date
)
select
    o.order_date,
    o.orders_count,
    o.buyers_count,
    o.total_amount,
    coalesce(i.items_sold, 0) as items_sold
from orders_daily as o
left join items_daily as i
    on o.order_date = i.order_date
order by o.order_date
