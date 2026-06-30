import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    TEST_DATABASE_URL: Optional[str] = os.getenv("TEST_DATABASE_URL")
    MONGODB_URL: Optional[str] = os.getenv("MONGODB_URL")
    DB_NAME: str = os.getenv("DB_NAME", "backend_db")
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")


settings = Settings()
