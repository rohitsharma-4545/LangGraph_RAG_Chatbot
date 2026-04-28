import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")
    CHROMA_DB_DIR = str((BASE_DIR / "chroma_db").resolve())

settings = Settings()