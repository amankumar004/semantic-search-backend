import os


class Settings:
    app_name: str = os.getenv("APP_NAME", "Semantic Search API")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    allowed_mime_type: str = os.getenv("ALLOWED_MIME_TYPE", "application/pdf")


settings = Settings()