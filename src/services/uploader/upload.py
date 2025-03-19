import redis
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
                    upload_file(data['file'], data['timestamp'])
                    redis_client.xack(steam_name, consumer_group, entry_id)  # Acknowledge message
                except Exception as e:
                    logger.error(f"Failed to upload file {data['file']}", e)
