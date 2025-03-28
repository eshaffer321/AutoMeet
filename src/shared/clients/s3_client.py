import boto3
from config.config import settings

# Ensure settings.s3 is properly defined and has the required attributes
s3 = boto3.client(
    's3',
    endpoint_url=getattr(settings.s3, 'url', None),
    aws_access_key_id=getattr(settings.s3, 'application_key_id', None),
    aws_secret_access_key=getattr(settings.s3, 'application_key', None),
)
