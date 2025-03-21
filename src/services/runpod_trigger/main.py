from shared.logging import logger
from config.config import settings
from shared.redis_client import redis_client
import redis

consumer_group = settings.runpod_trigger.consumer_group
steam_name = settings.redis.streams.audio_upload_complete_remote

consumer_name = "consumer_1"

try:
    redis_client.xgroup_create(steam_name, consumer_group, id='$', mkstream=True)
except redis.exceptions.ResponseError:
    pass  

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
                    s3_key = data['key']
                    redis_client.xack(steam_name, consumer_group, entry_id)  # Acknowledge message
                except Exception as e:
                    logger.error(f"Failed to trigger runpod for  {data['file']}: {str(e)}", exc_info=True)