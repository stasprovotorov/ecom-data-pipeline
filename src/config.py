import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    DB_URL: str
    CSV_USERS: str
    CSV_PRODUCTS: str
    CSV_ORDERS: str
    CSV_ORDER_ITEMS: str


settings = Settings(
    DB_URL=os.getenv('DB_URL'),
    CSV_USERS=os.getenv('CSV_USERS'),
    CSV_PRODUCTS=os.getenv('CSV_PRODUCTS'),
    CSV_ORDERS=os.getenv('CSV_ORDERS'),
    CSV_ORDER_ITEMS=os.getenv('CSV_ORDER_ITEMS'),
)
