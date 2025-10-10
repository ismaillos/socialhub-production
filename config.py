
import os
from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "changeme")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blotato.db")

engine = create_engine(DATABASE_URL, echo=True)

class Settings:
    encryption_key = ENCRYPTION_KEY
    engine = engine

settings = Settings()
