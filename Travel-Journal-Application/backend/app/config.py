from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb+srv://Saikrishna:Sai%4039311@cluster0.o5h9hve.mongodb.net/travel_journal_db?retryWrites=true&w=majority"
    DATABASE_NAME: str = "travel_journal_db"
    SECRET_KEY: str = "super-secret-jwt-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
