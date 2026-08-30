from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Базовые настройки
    app_name: str = "nyamstack"

    # PostgreSQL настройки
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    # Сборка URL .env -> app/config/config.py -> Settings
    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    # Настройки чтения .env файла (Pydantic v2)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()