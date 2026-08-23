from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Semantic Search API"
    database_url: str

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    embedding_model: str = "all-MiniLM-L6-v2"
    max_file_size_mb: int = 5
    allowed_mime_type: str = "application/pdf"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    jwt_secret_key: str = "development-secret-key-change-this"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30


settings = Settings()  # type: ignore[call-arg]