from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from pathlib import Path

_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")
    MONGO_URI: AnyUrl
    DB_NAME: str
    COLLECTION_NAME: str = "posts"

settings = Settings()
