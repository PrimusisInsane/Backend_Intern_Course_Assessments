from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DB_NAME: str = os.getenv("DB_NAME", "backend_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()