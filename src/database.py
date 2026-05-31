from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from src.config import settings


def get_engine() -> Engine:
    return create_engine(settings.DB_URL)
