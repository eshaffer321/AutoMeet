import boto3
from config.config import settings

s3 = boto3.client(
    's3',
    endpoint_url=settings.s3.url,
    aws_access_key_id=settings.s3.application_key_id,
    aws_secret_access_key=settings.s3.application_key
)
