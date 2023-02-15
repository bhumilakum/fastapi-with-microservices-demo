import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(verbose=True)


class Settings(BaseSettings):

    # database
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "postgresql")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_URI: str = f"{DB_SCHEMA}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # security auth token
    HASH_ALGORITHM: str = os.environ.get("HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRY_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRY_MINUTES")
    REFRESH_TOKEN_EXPIRY_MINUTES: int = os.environ.get("REFRESH_TOKEN_EXPIRY_MINUTES")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.environ.get("JWT_REFRESH_SECRET_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # case_sensitive = True


settings = Settings()
