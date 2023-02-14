import os
import dotenv
from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv(verbose=True)

class Settings(BaseSettings):
    # database
    DB_SCHEMA: str = os.getenv("DB_SCHEMA","postgresql")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_URI: str = f"{DB_SCHEMA}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    

    # ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES")
    # ALGORITHM = os.environ.get("ALGORITHM")
    # JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # should be kept secret
    # JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")  # should be kept secret

    # SQLALCHEMY_DATABASE_URI = f"{SCHEME}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # API_V1_STR = os.environ.get("API_V1_STR")
    # PROJECT_NAME = os.environ.get("PROJECT_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding="utf-8"
        # case_sensitive = True

        
settings = Settings()
