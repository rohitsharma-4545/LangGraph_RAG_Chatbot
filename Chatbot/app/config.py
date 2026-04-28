import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")
    CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")

settings = Settings()