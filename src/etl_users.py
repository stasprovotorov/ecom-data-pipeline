import pandas as pd
from sqlalchemy import text
from src import sql
from src.config import settings
from src.database import get_engine
from src.utils import normalize_string, get_source_filename, get_timestamp, extract_data_from_csv

EXPECTED_COLUMNS = {
    'user_id',
    'name',
    'email',
    'gender',
    'city',
    'signup_date',
}


def extract_users(filepath: str) -> pd.DataFrame:
    df_source = pd.read_csv(filepath)

    retrieved_columns = set(df_source.columns)
    missing_columns = EXPECTED_COLUMNS - retrieved_columns

    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    return df_source


def transform_users(df_source: pd.DataFrame, source_filename: str) -> pd.DataFrame:
    df_transformed = df_source.copy()

    for column in df_transformed.columns:
        df_transformed[column] = df_transformed[column].apply(normalize_string)    

    df_transformed['user_id'] = df_transformed['user_id'].str.upper()
    df_transformed['email'] = df_transformed['email'].str.lower()
    df_transformed['name'] = df_transformed['name'].str.title()
    df_transformed['gender'] = df_transformed['gender'].str.capitalize()
    df_transformed['city'] = df_transformed['city'].str.title()
    df_transformed['signup_date'] = pd.to_datetime(df_transformed['signup_date'], errors='coerce').dt.date

    df_transformed = df_transformed[df_transformed['user_id'].notna()]
    df_transformed = df_transformed[df_transformed['signup_date'].notna()]
    df_transformed = df_transformed.drop_duplicates(subset=['user_id'], keep='last')

    df_transformed['source_file'] = source_filename
    df_transformed['loaded_at'] = get_timestamp()

    return df_transformed[
        [
            'user_id',
            'name',
            'email',
            'gender',
            'city',
            'signup_date',
            'source_file',
            'loaded_at',
        ]
    ]


def load_users(df: pd.DataFrame) -> None:
    engine = get_engine()

    with engine.connect() as db:
        db.execute(text(sql.DROP_TABLE_TMP_USERS))
        db.execute(text(sql.CREATE_TABLE_TMP_USERS))

        df.to_sql(
            name='tmp_users',
            con=db,
            if_exists='append',
            index=False,
            method='multi',
        )

        db.execute(text(sql.INSERT_INTO_RAW_USERS))

        db.commit()


def main() -> None:
    source_filename = get_source_filename(settings.CSV_USERS)

    df_source = extract_data_from_csv(settings.CSV_USERS)
    df_transformed = transform_users(df_source, source_filename)
    load_users(df_transformed)


if __name__ == '__main__':
    main()    
