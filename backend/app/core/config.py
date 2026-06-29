from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentrix"
    API_V1_STR: str = "/api/v1"
    
    # Postgres
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "sentrix"
    POSTGRES_PASSWORD: str = "sentrix_pass"
    POSTGRES_DB: str = "sentrix_db"
    
    @property
    def sqlalchemy_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Qdrant
    QDRANT_URL: str = "http://qdrant:6333"

    # JWT Authentication
    SECRET_KEY: str = "super_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # AI Configuration
    AI_PROVIDER: str = "openai" # "openai", "claude", "gemini", "local"
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    LOCAL_LLM_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
