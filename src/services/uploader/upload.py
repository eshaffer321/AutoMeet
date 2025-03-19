import redis
from shared.redis_client import redis_client
from shared.logging import logging

from shared.config import settings

steam_name = settings.redis.streams.journal_steam_name
consumer_group = settings.uploader.consumer_group

try:
    redis_client.xgroup_create(steam_name, consumer_group, id='$', mkstream=True)
except redis.exceptions.ResponseError:
    pass  

consumer_name = "worker-1"

while True:
    logging.info(f"Waiting for messages from stream {steam_name}")
    
    messages = redis_client.xreadgroup(groupname=consumer_group, consumername=consumer_name,
                            streams={steam_name: ">"}, count=1, block=0)

    if messages:
        for stream_name, entries in messages:
            for entry_id, data in entries:
                logging.info(f"Processing: {data}")
                redis_client.xack(steam_name, consumer_group, entry_id)  # Acknowledge message