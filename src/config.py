from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f'{ROOT}/.env',
        env_file_encoding='utf-8',
    )

    DB_URL: str

    CSV_USERS: str
    CSV_ORDERS: str
    CSV_ORDER_ITEMS: str
    CSV_PRODUCTS: str


settings = Settings()
