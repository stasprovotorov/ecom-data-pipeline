CREATE TABLE IF NOT EXISTS raw_users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    gender TEXT,
    city TEXT,
    signup_date DATE,
    source_file TEXT,
    loaded_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS raw_products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    price NUMERIC(10, 2),
    rating NUMERIC(3, 2),
    source_file TEXT,
    loaded_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS raw_orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES raw_users(user_id),
    order_date TIMESTAMPTZ,
    order_status TEXT,
    total_amount NUMERIC(10, 2),
    source_file TEXT,
    loaded_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS raw_order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES raw_orders(order_id),
    product_id TEXT NOT NULL REFERENCES raw_products(product_id),
    user_id TEXT NOT NULL REFERENCES raw_users(user_id),
    quantity INTEGER,
    item_price NUMERIC(10, 2),
    item_total NUMERIC(10, 2),
    source_file TEXT,
    loaded_at TIMESTAMPTZ
);
