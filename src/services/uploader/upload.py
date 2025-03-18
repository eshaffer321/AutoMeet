import redis
import os
import logging

from config.config import UPLOADER_CONSUMER_GROUP
REDIS_HOST = os.getenv("REDIS_HOST", "redis_local")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_STREAM = os.getenv("REDIS_STREAM", "journal")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


try:
    r.xgroup_create(REDIS_STREAM, UPLOADER_CONSUMER_GROUP, id='$', mkstream=True)
except redis.exceptions.ResponseError:
    pass  

consumer_name = "worker-1"

while True:
    logging.info(f"Waiting for messages from stream {REDIS_STREAM}")
    
    messages = r.xreadgroup(groupname=UPLOADER_CONSUMER_GROUP, consumername=consumer_name,
                            streams={REDIS_STREAM: ">"}, count=1, block=0)

    if messages:
        for stream_name, entries in messages:
            for entry_id, data in entries:
                print(f"Processing: {data}")
                r.xack(REDIS_STREAM, UPLOADER_CONSUMER_GROUP, entry_id)  # Acknowledge message