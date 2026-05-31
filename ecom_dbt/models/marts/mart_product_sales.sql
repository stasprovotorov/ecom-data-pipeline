select
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    count(i.order_item_id) as order_item_count,
    coalesce(sum(i.quantity), 0) as sold_count,
    round(coalesce(sum(i.item_total), 0), 2) as total_amount,
    round(coalesce(avg(i.item_price), 0), 2) as avg_item_price
from {{ ref('stg_products') }} as p
left join {{ ref('stg_order_items') }} as i
    on p.product_id = i.product_id
group by
    p.product_id,
    p.product_name,
    p.category,
    p.brand
