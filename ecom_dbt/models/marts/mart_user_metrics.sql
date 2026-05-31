select
    u.user_id,
    u.name,
    u.email,
    u.city,
    u.signup_date,
    count(o.order_id) as order_count,
    coalesce(sum(o.total_amount), 0) as total_amount,
    round(coalesce(avg(o.total_amount), 0), 2) as avg_amount,
    min(o.order_date)::date as first_order,
    max(o.order_date)::date as last_order
from {{ ref('stg_users') }} as u 
left join {{ ref('stg_orders') }} as o 
    on u.user_id = o.user_id
group by
    u.user_id,
    u.name,
    u.email,
    u.city,
    u.signup_date
