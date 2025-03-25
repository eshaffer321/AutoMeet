import redis
from shared.logging import logger
from config.config import settings
from shared.redis_client import redis_client

def consume_stream():
    consumer_group = settings.runpod_trigger.consumer_group
    stream_name = settings.redis.streams.audio_upload_complete_remote
    consumer_name = "consumer_1"

    try:
        redis_client.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
    except redis.exceptions.ResponseError:
        pass  # Group already exists

    while True:
        logger.info(f"Waiting for messages from stream {stream_name}")

        messages = redis_client.xreadgroup(
            groupname=consumer_group,
            consumername=consumer_name,
            streams={stream_name: ">"},
            count=1,
            block=0
        )

        if messages:
            for _, entries in messages:
                for entry_id, data in entries:
                    logger.info(f"Processing: {data}")
                    try:
                        s3_key = data['key']
                        # TODO: Trigger RunPod call here
                        redis_client.xack(stream_name, consumer_group, entry_id)
                    except Exception as e:
                        logger.error(f"❌ Failed to trigger runpod for {data.get('file')}: {str(e)}", exc_info=True)