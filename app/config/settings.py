from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Semantic Search API"
    database_url: str

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None

    embedding_model: str
    max_file_size_mb: int
    allowed_mime_type: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int


settings = Settings()  # type: ignore[call-arg]