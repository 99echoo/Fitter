from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://fitter:fitter_password@localhost:5432/fitter"

    # AI API Keys
    google_api_key: str = ""
    kling_api_key: str = ""

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = True

    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # File Upload
    max_upload_size_mb: int = 10
    upload_dir: str = "uploads"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
