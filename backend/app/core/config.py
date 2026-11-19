import os

from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

REDIS_URL = os.getenv("REDIS_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

RATE_LIMIT_CAPACITY = int(
    os.getenv("RATE_LIMIT_CAPACITY", 20)
)

RATE_LIMIT_REFILL_RATE = float(
    os.getenv("RATE_LIMIT_REFILL_RATE", 1)
)