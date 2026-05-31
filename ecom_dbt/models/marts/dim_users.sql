SELECT
    user_id,
    name,
    email,
    gender,
    city,
    signup_date,
    source_file,
    loaded_at
FROM 
    {{ ref('stg_users') }}
