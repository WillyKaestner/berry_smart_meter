from typing import Optional
from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_name: Optional[str] = None
    database_password: Optional[str] = None
    database_username: Optional[str] = None
    database_host: Optional[str] = None
    papertrail_host: Optional[str] = None
    papertrail_port: Optional[int] = None

    class Config:
        env_file = f"{Path(__file__).resolve().parent}/.env"


SETTINGS = Settings()
