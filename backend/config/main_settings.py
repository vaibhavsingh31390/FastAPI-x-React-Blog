import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Security

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")


class SETTINGS:
    PROJECT_NAME: str = "FastAPI"
    PROJECT_VERSION: str = "0.1.0"
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "postgres")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SECURITY_ALGO: str = os.getenv("SECURITY_ALGO", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    DATABASE_URL: str = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        if DB_PASSWORD
        else f"postgresql://{DB_USERNAME}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
