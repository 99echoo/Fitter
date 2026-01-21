from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

_REPO_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILES = [
    _REPO_ROOT / ".env",
    _REPO_ROOT / "backend" / ".env",
]


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://fitter:fitter_password@localhost:5432/fitter"

    # AI API Keys
    openai_api_key: str = ""
    openai_organization: str = ""
    openai_project: str = ""
    kling_api_key: str = ""
    kling_access_key: str = ""
    kling_secret_key: str = ""
    openai_image_model: str = "gpt-image-1.5"
    openai_image_max_side: int = 1536
    openai_image_max_mb: int = 10
    openai_image_jpeg_quality: int = 85
    openai_image_force_jpeg: bool = True
    openai_image_output_size: str = "1024x1536"
    openai_image_output_format: str = "png"
    openai_image_quality: str = "auto"
    openai_image_n: int = 1
    openai_image_max_inputs: int = 5
    kling_base_url: str = "https://api-singapore.klingai.com"
    kling_model_name: str = "kling-v1"
    kling_mode: str = "pro"
    kling_duration: str = "5"

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
        env_file = [str(path) for path in _ENV_FILES]
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
