from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel
from typing import Literal, Optional


class LoggerSettings(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    format: Literal["json", "text"] = "text"
    output: Literal["console", "file", "both"] = "both"
    file_name: str = "./logs/app.log"
    rotation: Literal["size", "time"] = "time"
    max_bytes: Optional[int] = Field(10 * 1024 * 1024, gt=0, description="Bytes for rotation")
    backup_count: int = Field(7, ge=0)


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

    # logger相关
    LOGGER: LoggerSettings = LoggerSettings()


settings = Settings()
