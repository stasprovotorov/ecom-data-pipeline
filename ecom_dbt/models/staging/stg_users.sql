select
    user_id,
    name,
    email,
    gender,
    city,
    signup_date,
    source_file,
    loaded_at
from
    {{ source('raw', 'raw_users') }}
