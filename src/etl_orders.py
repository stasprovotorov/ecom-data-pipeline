import pandas as pd
from sqlalchemy import text
from src import sql
from src.config import settings
from src.database import get_engine
from src.utils import normalize_string, get_timestamp, get_source_filename

EXPECTED_COLUMNS = {
    'order_id',
    'user_id',
    'order_date',
    'order_status',
    'total_amount',
}


def extract_orders(filepath: str) -> pd.DataFrame:
    df_source = pd.read_csv(filepath)

    retrieved_columns = set(df_source.columns)
    missing_columns = EXPECTED_COLUMNS - retrieved_columns

    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    return df_source


def transform_orders(df_source: pd.DataFrame, source_filename: str) -> pd.DataFrame:
    df_transformed = df_source.copy()

    for column in df_transformed.columns:
        df_transformed[column] = df_transformed[column].apply(normalize_string)

    df_transformed['user_id'] = df_transformed['user_id'].str.upper()
    df_transformed['order_date'] = pd.to_datetime(df_transformed['order_date'], errors='coerce')
    df_transformed['order_status'] = df_transformed['order_status'].str.upper()
    df_transformed['total_amount'] = df_transformed['total_amount'].apply(lambda x: float(x))

    df_transformed = df_transformed[df_transformed['order_id'].notna()]
    df_transformed = df_transformed[df_transformed['user_id'].notna()]
    df_transformed = df_transformed.drop_duplicates(subset=['order_id'], keep='last')

    df_transformed['source_file'] = source_filename
    df_transformed['loaded_at'] = get_timestamp()

    return df_transformed[
        [
            'order_id',
            'user_id',
            'order_date',
            'order_status',
            'total_amount',
            'source_file',
            'loaded_at',
        ]
    ]


def load_orders(df: pd.DataFrame) -> None:
    engine = get_engine()

    with engine.connect() as db:
        db.execute(text(sql.DROP_TABLE_TMP_ORDERS))
        db.execute(text(sql.CREATE_TABLE_TMP_ORDERS))

        df.to_sql(
            name='tmp_orders',
            con=db,
            if_exists='append',
            index=False,
            method='multi',
        )

        db.execute(text(sql.INSERT_INTO_RAW_ORDERS))

        db.commit()


def main() -> None:
    source_filename = get_source_filename(settings.CSV_ORDERS)

    df_source = extract_orders(settings.CSV_ORDERS)
    df_transformed = transform_orders(df_source, source_filename)
    load_orders(df_transformed)


if __name__ == '__main__':
    main()
