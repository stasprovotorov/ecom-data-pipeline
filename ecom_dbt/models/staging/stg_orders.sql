select
    order_id,
    user_id,
    order_date,
    order_status,
    total_amount,
    source_file,
    loaded_at
from
    {{ source('raw', 'raw_orders') }}
