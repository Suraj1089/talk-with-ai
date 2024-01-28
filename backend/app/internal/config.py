from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    PROJECT_NAME: str = 'fastapi-tutorials'
    DATABASE_URI: str
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
    


@lru_cache
def get_settings():
    return Settings()
