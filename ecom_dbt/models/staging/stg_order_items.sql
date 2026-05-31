select
    order_item_id,
    order_id,
    product_id,
    user_id,
    quantity,
    item_price,
    item_total,
    source_file,
    loaded_at
from
    {{ source('raw', 'raw_order_items') }}
