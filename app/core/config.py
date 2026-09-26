from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict

class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    COMPANY_SECRETS: Dict[str, str]

    # Ye line Pydantic ko batati hai ke in variables ki values kahan se lani hain
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
   
# Is 'settings' object ko hum pure project me import karenge
settings = Settings()