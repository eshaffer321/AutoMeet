import redis
import os
from datetime import datetime
from config.config import settings
from shared.redis_client import redis_client
from shared.s3_client import s3
from shared.logging import logger 

steam_name = settings.redis.streams.journal_steam_name
consumer_group = settings.uploader.consumer_group

try:
    redis_client.xgroup_create(steam_name, consumer_group, id='$', mkstream=True)
except redis.exceptions.ResponseError:
    pass  

consumer_name = "worker-1"

def upload_file(filepath, timestamp):
    filename = os.path.basename(filepath)
    file_path = f"{settings.uploader.audio_dir}/{filename}"
    dt = datetime.fromisoformat(timestamp.replace("Z", ""))  # Remove Z for parsing
    date_path = dt.strftime("%Y/%m/%d")  # YYYY/MM/DD structure
    time_part = dt.strftime("%H%M")  # HHMM format for time-based uniqueness

    s3_key = f"audio/{date_path}/{time_part}_{filename}"
    
    logger.info(f"Starting upload of file {file_path}")
    s3.upload_file(file_path,settings.s3.bucket_name,s3_key, ExtraArgs={})
    logger.info(f'Successfull uploaded {file_path}')
    publish_message(s3_key)


def publish_message(s3_key):
    message = {"key": s3_key}
    steam_name = settings.redis.steams.audio_upload_complete_remote \
        if settings.uploader.run_mode == "runpod" \
        else settings.redis.streams.audio_upload_complete_local 

    logger.info(f"Signalling for processing of {s3_key} to {steam_name}")
    redis_client.xadd(steam_name, message)
 
while True:
    logger.info(f"Waiting for messages from stream {steam_name}")
    
    messages = redis_client.xreadgroup(
        groupname=consumer_group,
        consumername=consumer_name,
        streams={steam_name: ">"},
        count=1,
        block=0
    )

    if messages:
        for _, entries in messages:
            for entry_id, data in entries:
                logger.info(f"Processing: {data}")
                try:
                    upload_file(data['file'], data['timestamp'])
                    redis_client.xack(steam_name, consumer_group, entry_id)  # Acknowledge message
                except Exception as e:
                    logger.error(f"Failed to upload file {data['file']}: {str(e)}", exc_info=True)