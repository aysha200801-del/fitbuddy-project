from dotenv import load_dotenv
import os

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY").strip()
GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.5-flash")
GEMINI_TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-3.5-flash")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")
