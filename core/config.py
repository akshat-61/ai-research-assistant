from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_research.db"
    
    # Security
    JWT_SECRET: str = "jwt_secret_key_for_python_fastapi"
    
    # LLM Configuration
    LLM_BASE_URL: str = "http://10.10.8.200:5000/v1"
    MODEL_NAME: str = "google/gemma-4-26b-a4b-qat"
    EMBEDDING_MODEL: str = "nomic-embed-text"
    TEMPERATURE: float = 0.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
