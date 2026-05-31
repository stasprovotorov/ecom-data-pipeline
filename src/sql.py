DROP_TABLE_TMP_USERS = """
    DROP TABLE IF EXISTS tmp_users;
"""

DROP_TABLE_TMP_ORDERS = """
    DROP TABLE IF EXISTS tmp_orders;
"""

DROP_TABLE_TMP_ORDER_ITEMS = """
    DROP TABLE IF EXISTS tmp_order_items;
"""

DROP_TABLE_TMP_PRODUCTS = """
    DROP TABLE IF EXISTS tmp_products;
"""

CREATE_TABLE_TMP_USERS = """
    CREATE TEMP TABLE tmp_users (
        user_id TEXT,
        name TEXT,
        email TEXT,
        gender TEXT,
        city TEXT,
        signup_date DATE,
        source_file TEXT,
        loaded_at TIMESTAMPTZ
    );
"""

CREATE_TABLE_TMP_ORDERS = """
    CREATE TEMP TABLE tmp_orders (
        order_id TEXT,
        user_id TEXT,
        order_date TIMESTAMPTZ,
        order_status TEXT,
        total_amount NUMERIC(10, 2),
        source_file TEXT,
        loaded_at TIMESTAMPTZ
    );
"""

CREATE_TABLE_TMP_ORDER_ITEMS = """
    CREATE TEMP TABLE tmp_order_items (
        order_item_id TEXT,
        order_id TEXT,
        product_id TEXT,
        user_id TEXT,
        quantity INTEGER,
        item_price NUMERIC(10, 2),
        item_total NUMERIC(10, 2),
        source_file TEXT,
        loaded_at TIMESTAMPTZ
    );
"""

CREATE_TABLE_TMP_PRODUCTS = """
    CREATE TEMP TABLE tmp_products (
        product_id TEXT,
        product_name TEXT,
        category TEXT,
        brand TEXT,
        price NUMERIC(10, 2),
        rating NUMERIC(10, 2),
        source_file TEXT,
        loaded_at TIMESTAMPTZ
    );
"""

INSERT_INTO_RAW_USERS = """
    INSERT INTO raw_users (
        user_id,
        name,
        email,
        gender,
        city,
        signup_date,
        source_file,
        loaded_at
    )
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
        tmp_users
    ON CONFLICT (user_id)
    DO UPDATE SET
        name = EXCLUDED.name,
        email = EXCLUDED.email,
        gender = EXCLUDED.gender,
        city = EXCLUDED.city,
        signup_date = EXCLUDED.signup_date,
        source_file = EXCLUDED.source_file,
        loaded_at = EXCLUDED.loaded_at;
"""

INSERT_INTO_RAW_ORDERS = '''
    INSERT INTO raw_orders (
        order_id,
        user_id,
        order_date,
        order_status,
        total_amount,
        source_file,
        loaded_at
    )
    SELECT
        order_id,
        user_id,
        order_date,
        order_status,
        total_amount,
        source_file,
        loaded_at
    FROM
        tmp_orders
    ON CONFLICT (order_id)
    DO UPDATE SET
        user_id = EXCLUDED.user_id,
        order_date = EXCLUDED.order_date,
        order_status = EXCLUDED.order_status,
        total_amount = EXCLUDED.total_amount,
        source_file = EXCLUDED.source_file,
        loaded_at = EXCLUDED.loaded_at;
'''

INSERT_INTO_RAW_ORDER_ITEMS = """
    INSERT INTO raw_order_items (
        order_item_id,
        order_id,
        product_id,
        user_id,
        quantity,
        item_price,
        item_total,
        source_file,
        loaded_at
    )
    SELECT
        order_item_id,
        order_id,
        product_id,
        user_id,
        quantity,
        item_price,
        item_total,
        source_file,
        loaded_at
    FROM
        tmp_order_items
    ON CONFLICT (order_item_id)
    DO UPDATE SET
        order_id = EXCLUDED.order_id,
        product_id = EXCLUDED.product_id,
        user_id = EXCLUDED.user_id,
        quantity = EXCLUDED.quantity,
        item_price = EXCLUDED.item_price,
        item_total = EXCLUDED.item_total,
        source_file = EXCLUDED.source_file,
        loaded_at = EXCLUDED.loaded_at
"""

INSERT_INTO_RAW_PRODUCTS = """
    INSERT INTO raw_products (
        product_id,
        product_name,
        category,
        brand,
        price,
        rating,
        source_file,
        loaded_at
    )
    SELECT
        product_id,
        product_name,
        category,
        brand,
        price,
        rating,
        source_file,
        loaded_at
    FROM
        tmp_products
    ON CONFLICT (product_id)
    DO UPDATE SET
        product_name = EXCLUDED.product_name,
        category = EXCLUDED.category,
        brand = EXCLUDED.brand,
        price = EXCLUDED.price,
        rating = EXCLUDED.rating,
        source_file = EXCLUDED.source_file,
        loaded_at = EXCLUDED.loaded_at
"""
