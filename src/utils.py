import os
import re
from datetime import datetime
import pandas as pd
from logging import Logger


def get_source_filename(filepath: str) -> str:
    return os.path.basename(filepath)


def get_timestamp() -> datetime:
    return datetime.now()


def normalize_string(value: str) -> str | None:
    if not isinstance(value, str):
        if pd.isna(value):
            return None
        return value

    value = value.strip()

    if not value:
        return None    
    return value


def get_csv_file_row_count(filepath: str, is_header: bool = False) -> int:
    with open(filepath, 'r', encoding='utf-8') as file:
        row_count = sum(1 for _ in file)
    
    if is_header:
        return row_count - 1
    return row_count


def extract_data_from_csv(filepath: str, required_columns: set, logger: Logger, is_header: bool = True) -> pd.DataFrame:
    logger.info("Exctracting data from CSV file: %s", filepath)

    df_source = pd.read_csv(filepath)

    retrieved_columns = set(df_source.columns)
    missing_columns = required_columns - retrieved_columns

    if missing_columns:
        logger.error("Missing expected columns: %s", missing_columns)
        raise ValueError(f"Missing expected columns: {missing_columns}")
    
    df_source['src_row_num'] = df_source.index + 1

    file_row_count = get_csv_file_row_count(filepath, is_header)
    df_row_count = len(df_source)

    if file_row_count != df_row_count:
        logger.warning("Source file's and extracted dataframe's row counts not equals. File: %s, dataframe: %s", file_row_count, df_row_count)

    return df_source


def is_valid_email(email: str) -> bool:
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_regex.match(email))


def is_valid_user_id(user_id: str) -> bool:
    user_id_regex = re.compile(r'^U\d{6}$')
    return bool(user_id_regex.match(user_id))
