select
    product_id,
    product_name,
    category,
    brand,
    price,
    rating,
    source_file,
    loaded_at
from
    {{ source('raw', 'raw_products') }}
