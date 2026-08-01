import os


class Settings:
    app_name: str = os.getenv("APP_NAME", "Semantic Search API")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()
