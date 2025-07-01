from urllib.parse import quote_plus

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str
    ECHO: bool = False


class Settings(BaseSettings):
    # Настройки фоновой проверки
    ENABLE_BACKGROUND_CHECK: bool = False
    BACKGROUND_CHECK_INTERVAL_SECONDS: int = 300  # 5 минут по умолчанию

    DB: DBSettings

    @property
    def DATABASE_URL(self) -> str:
        # Экранируем спецсимволы в пароле
        password = quote_plus(self.DB.PASSWORD)
        return (
            f"postgresql+asyncpg://{self.DB.USER}:{password}"
            f"@{self.DB.HOST}:{self.DB.PORT}/{self.DB.NAME}"
        )

    # Можно добавить другие настройки, например, для будущей аутентификации

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",  # Игнорировать лишние переменные в .env
    )


settings = Settings()
