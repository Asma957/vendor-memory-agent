"""Settings are read from .env (local) or st.secrets (Streamlit Cloud)."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")


def get_setting(name, default=None):
    val = os.getenv(name)
    if val:
        return val
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default


HINDSIGHT_BASE_URL = get_setting("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
HINDSIGHT_API_KEY = get_setting("HINDSIGHT_API_KEY")
GROQ_API_KEY = get_setting("GROQ_API_KEY")
BANK_ID = get_setting("VENDOR_BANK_ID", "vendor-memory-agent")
GROQ_MODEL = get_setting("GROQ_MODEL", "openai/gpt-oss-120b")
GROQ_FALLBACK_MODEL = "qwen/qwen3-32b"
USER_NAME = get_setting("USER_NAME", "Asma")
