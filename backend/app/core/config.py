from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    ENV: str = "dev"
    APP_NAME: str = "RISA"

    # DB
    DATABASE_URL: str = "postgresql+asyncpg://risaadmin:risa2026!Dev@localhost:5432/risadb"

    # Auth
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # CORS — 환경변수에서 콤마 구분 문자열로 받아서 파싱
    ALLOWED_ORIGINS_STR: str = "http://localhost:5173"

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS_STR.split(",")]

    # External APIs
    ANTHROPIC_API_KEY: str = ""
    CLOVA_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
