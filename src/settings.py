import enum
import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Stage(enum.StrEnum):
    LOCAL = "LOCAL"
    STAGING = "STAGING"
    PROD = "PROD"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="local.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    STAGE: Stage = Stage.LOCAL
    SERVICE_VERSION: str = "0.1.0"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str | None = None

    @property
    def create_database_url(self) -> str:
        db_name = self.POSTGRES_DB
        print(db_name)
        if os.getenv("PYTEST_CURRENT_TEST") and self.POSTGRES_TEST_DB:
            db_name = self.POSTGRES_TEST_DB

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=f"{db_name}",  # TODO f-string use?
            )
        )


settings = Settings()
