from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://Saikrishna:Sai%4039311@cluster0.o5h9hve.mongodb.net/travel_journal_db?retryWrites=true&w=majority")
    DATABASE_NAME: str = "travel_journal_db"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-jwt-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    # DEBUG: First try to get from environment, log if missing
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "sk-proj-TEMP-TEST-KEY")  # ⚠️ TEMPORARY

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Debug logging
import sys
print(f"DEBUG: OPENAI_API_KEY loaded: {bool(settings.OPENAI_API_KEY)}", file=sys.stderr)
print(f"DEBUG: OPENAI_API_KEY length: {len(settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else 0}", file=sys.stderr)
