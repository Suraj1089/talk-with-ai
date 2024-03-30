from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    PROJECT_NAME: str = 'fastapi-tutorials'
    DATABASE_URI: str
    DATABASE_KEY: str
    WEBSITE_DOMAIN: str = 'http://localhost:8000'
    SECRET_KEY: str
    ALGORITHM: str
    EMAILS_ENABLED: bool = False
    SMTP_HOST: str = 587
    SMTP_PORT: int
    SMTP_LOGIN: str
    SMTP_PASSWORD: str
    SMTP_API_KEY: str
    EMAILS_FROM_NAME: str
    EMAILS_FROM_EMAIL: str
    EMAIL_TEMPLATES_DIR: str = None
    ELEVEN_LABS_API_KEY: str
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    OPENAI_ORG: str
    OPENAI_API_KEY: str


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "mycoolapp"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },

    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


@lru_cache
def get_settings():
    return Settings()
