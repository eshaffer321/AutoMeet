import os
from datetime import datetime
from config.config import settings
from shared.clients.redis_client import RedisStreamConsumer
from shared.clients.s3_client import s3
from shared.util.logging import logger


consumer = RedisStreamConsumer(
    stream_name=settings.redis.streams.journal_steam_name,
    consumer_group=settings.uploader.consumer_group,
    consumer_name="worker-1"
)

def upload_file(filepath, timestamp):
    filename = os.path.basename(filepath)
    file_path = f"{settings.uploader.audio_dir}/{filename}"
    dt = datetime.fromisoformat(timestamp.replace("Z", ""))  # Remove Z for parsing
    date_path = dt.strftime("%Y/%m/%d")  # YYYY/MM/DD structure
    time_part = dt.strftime("%H%M")  # HHMM format for time-based uniqueness

    s3_key = f"audio/{date_path}/{time_part}_{filename}"
    
    logger.info(f"Starting upload of file {file_path}")
    s3.upload_file(file_path,settings.s3.bucket_name,s3_key)
    logger.info(f'Successfull uploaded {file_path}')
    return s3_key


def publish_message(s3_key):
    message = {"key": s3_key}
    steam_name = settings.redis.streams.audio_upload_complete_remote \
        if settings.uploader.run_mode == "runpod" \
        else settings.redis.streams.audio_upload_complete_local 

    logger.info(f"Signalling for processing of {s3_key} to {steam_name}")
    consumer.client.xadd(steam_name, message)

def handler(data):
    s3_key = upload_file(data['file'], data['timestamp'])
    publish_message(s3_key)

def consume_stream():
    consumer.process(handler_fn=handler)
