import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/research_assistant"
    SECRET_KEY: str = "your-super-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    UPLOAD_DIR: str = "./data/uploads"
    REPORTS_DIR: str = "./data/reports"
    SAMPLE_DATASETS_DIR: str = "./data/sample_datasets"
    SAMPLE_PAPERS_DIR: str = "./data/sample_papers"
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"        # <-- this is the fix, ignores extra .env fields

settings = Settings()

for directory in [
    settings.UPLOAD_DIR,
    settings.REPORTS_DIR,
    settings.CHROMA_PERSIST_DIR,
    settings.SAMPLE_DATASETS_DIR,
    settings.SAMPLE_PAPERS_DIR,
]:
    Path(directory).mkdir(parents=True, exist_ok=True)