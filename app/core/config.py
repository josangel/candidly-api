from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General
    app_name: str = "Candidly API"
    environment: str = Field("development", env="ENVIRONMENT")

    # Database
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: int = Field(..., env="POSTGRES_PORT")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")

    # Redis (Celery broker)
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")

    # S3
    s3_endpoint: str = Field(..., env="S3_ENDPOINT")
    s3_bucket: str = Field(..., env="S3_BUCKET")
    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")

    # AssemblyAI
    assemblyai_api_key: str = Field(..., env="ASSEMBLYAI_API_KEY")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"  # noqa: E501
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    CELERY_BROKER_URL: str = "redis://redis:6379/0"


settings = Settings()
