"""Module for managing application settings and configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=Path(".") / env_file)


class Settings(BaseSettings):
    env: str = "local"
    s3_endpoint: str = "http://localhost:9000"
    s3_bucket: str = "local-bucket"
    aws_access_key_id: str = "local-access-key"
    aws_secret_access_key: str = "local-secret-key"
    assembly_mock: bool = True

    model_config = {
        "env_file": env_file,
        "env_file_encoding": "utf-8",
    }


settings = Settings()
