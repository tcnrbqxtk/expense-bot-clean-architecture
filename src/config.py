import os

from dotenv import load_dotenv


load_dotenv()

ENV: str = os.getenv("ENV", "PROD")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_IDS: list[str] = os.getenv("ADMIN_IDS", "").split(",")
DATA_FILE: str = os.getenv("DATA_FILE", "data/expenses.json")

# DB_URL: str = os.getenv("DB_URL", "postgresql+asyncpg://postgres:your_password@db:5432/expenses_db")
