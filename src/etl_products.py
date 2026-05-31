import pandas as pd
from sqlalchemy import text
from src import sql
from src.config import settings
from src.database import get_engine
from src.utils import normalize_string, get_source_filename, get_timestamp

EXPECTED_COLUMNS = {
    'product_id',
    'product_name',
    'category',
    'brand',
    'price',
    'rating',
}


def extract_products(filepath: str) -> pd.DataFrame:
    df_source = pd.read_csv(filepath)

    retrieved_columns = set(df_source.columns)
    missing_columns = EXPECTED_COLUMNS - retrieved_columns

    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    return df_source


def transform_products(df_source: pd.DataFrame, source_filename: str) -> pd.DataFrame:
    df_transformed = df_source.copy()

    for column in df_transformed.columns:
        df_transformed[column] = df_transformed[column].apply(normalize_string)    

    df_transformed['product_id'] = df_transformed['product_id'].str.upper()
    df_transformed['product_name'] = df_transformed['product_name'].str.title()
    df_transformed['category'] = df_transformed['category'].str.upper()
    df_transformed['brand'] = df_transformed['brand'].str.title()
    df_transformed['price'] = df_transformed['price'].apply(lambda x: float(x))
    df_transformed['rating'] = df_transformed['rating'].apply(lambda x: float(x))

    df_transformed = df_transformed[df_transformed['product_id'].notna()]
    df_transformed = df_transformed.drop_duplicates(subset=['product_id'], keep='last')

    df_transformed['source_file'] = source_filename
    df_transformed['loaded_at'] = get_timestamp()

    return df_transformed[
        [
            'product_id',
            'product_name',
            'category',
            'brand',
            'price',
            'rating',
            'source_file',
            'loaded_at',
        ]
    ]


def load_products(df: pd.DataFrame) -> None:
    engine = get_engine()

    with engine.connect() as db:
        db.execute(text(sql.DROP_TABLE_TMP_PRODUCTS))
        db.execute(text(sql.CREATE_TABLE_TMP_PRODUCTS))

        df.to_sql(
            name='tmp_products',
            con=db,
            if_exists='append',
            index=False,
            method='multi',
        )

        db.execute(text(sql.INSERT_INTO_RAW_PRODUCTS))

        db.commit()


def main() -> None:
    source_filename = get_source_filename(settings.CSV_PRODUCTS)

    df_source = extract_products(settings.CSV_PRODUCTS)
    df_transformed = transform_products(df_source, source_filename)
    load_products(df_transformed)


if __name__ == '__main__':
    main()
