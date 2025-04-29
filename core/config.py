"""Module for application configuration settings."""

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    env: str = "local"
    s3_endpoint: AnyUrl
    s3_bucket: str
    assembly_mock: bool = True
    aws_access_key_id: str
    aws_secret_access_key: str

    class Config:
        env_file = ".env"


settings = Settings()
