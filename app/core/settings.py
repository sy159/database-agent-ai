from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    APP_NAME: str = Field("database-agent-ai", env="APP_NAME")
    DEBUG: bool = Field(True, env="DEBUG")
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")

    DATABASE_URL: str = Field("mysql://root:zx123@localhost:3306/test", env="DATABASE_URL")


settings = Settings()
