import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class Config:
    """
    Centralized configuration management.
    """

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "gemini-2.5-flash")
    FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "llama3")
    OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

    VECTOR_STORE_PATH = str(BASE_DIR / "data" / "vector_store")
    TEMP_UPLOAD_PATH = str(BASE_DIR / "data" / "temp_uploads")
