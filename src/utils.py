import os
from datetime import datetime
import pandas as pd


def get_source_filename(filepath: str) -> str:
    return os.path.basename(filepath)


def get_timestamp() -> datetime:
    return datetime.now()


def normalize_string(value: str) -> str | None:
    if not isinstance(value, str):
        return value

    if pd.isna(value):
        return None
    
    value = value.strip()
    if not value:
        return None
    
    return value
