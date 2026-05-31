import pandas as pd
from sqlalchemy import text
from src import sql
from src.config import settings
from src.database import get_engine
from src.utils import normalize_string, get_source_filename, get_timestamp

EXPECTED_COLUMNS = {
    'order_item_id',
    'order_id',
    'product_id',
    'user_id',
    'quantity',
    'item_price',
    'item_total',
}

def extract_order_items(filepath: str) -> pd.DataFrame:
    df_source = pd.read_csv(filepath)

    retrieved_columns = set(df_source.columns)
    missing_columns = EXPECTED_COLUMNS - retrieved_columns

    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    return df_source


def transform_order_items(df_source: pd.DataFrame, source_filename: str) -> pd.DataFrame:
    df_transformed = df_source.copy()

    for column in df_transformed.columns:
        df_transformed[column] = df_transformed[column].apply(normalize_string)    

    df_transformed['order_item_id'] = df_transformed['order_item_id'].str.upper()
    df_transformed['order_id'] = df_transformed['order_id'].str.upper()
    df_transformed['product_id'] = df_transformed['product_id'].str.upper()
    df_transformed['user_id'] = df_transformed['user_id'].str.upper()
    df_transformed['quantity'] = df_transformed['quantity'].apply(lambda x: int(x))
    df_transformed['item_price'] = df_transformed['item_price'].apply(lambda x: float(x))
    df_transformed['item_total'] = df_transformed['item_total'].apply(lambda x: float(x))

    df_transformed = df_transformed[df_transformed['order_item_id'].notna()]
    df_transformed = df_transformed[df_transformed['order_id'].notna()]
    df_transformed = df_transformed[df_transformed['product_id'].notna()]
    df_transformed = df_transformed[df_transformed['user_id'].notna()]
    df_transformed = df_transformed.drop_duplicates(subset=['order_item_id'], keep='last')

    df_transformed['source_file'] = source_filename
    df_transformed['loaded_at'] = get_timestamp()

    return df_transformed[
        [
            'order_item_id',
            'order_id',
            'product_id',
            'user_id',
            'quantity',
            'item_price',
            'item_total',
            'source_file',
            'loaded_at',
        ]
    ]


def load_users(df: pd.DataFrame) -> None:
    engine = get_engine()

    with engine.connect() as db:
        db.execute(text(sql.DROP_TABLE_TMP_ORDER_ITEMS))
        db.execute(text(sql.CREATE_TABLE_TMP_ORDER_ITEMS))

        df.to_sql(
            name='tmp_order_items',
            con=db,
            if_exists='append',
            index=False,
            method='multi',
        )

        db.execute(text(sql.INSERT_INTO_RAW_ORDER_ITEMS))

        db.commit()


def main() -> None:
    source_filename = get_source_filename(settings.CSV_ORDER_ITEMS)

    df_source = extract_order_items(settings.CSV_ORDER_ITEMS)
    df_transformed = transform_order_items(df_source, source_filename)
    load_users(df_transformed)


if __name__ == '__main__':
    main()    
