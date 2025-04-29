"""Module for uploading files to S3."""

import boto3

from core.config import settings

s3 = boto3.client(
    "s3",
    endpoint_url=settings.s3_endpoint,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def upload_audio(file, filename: str) -> str:
    s3.upload_fileobj(file.file, settings.s3_bucket, filename)
    return f"{settings.s3_endpoint}/{settings.s3_bucket}/{filename}"
