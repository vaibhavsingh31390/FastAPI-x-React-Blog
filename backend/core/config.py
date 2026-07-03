import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "FastAPI"
    PROJECT_VERSION: str = "0.1.0"
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "postgres")

    if DB_PASSWORD:
        DATABASE_URL: str = (
            f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        DATABASE_URL: str = f"postgresql://{DB_USERNAME}@{DB_HOST}:{DB_PORT}/{DB_NAME}"