import redis
from shared.logging import logger
from config.config import settings
from shared.redis_client import RedisStreamConsumer
from shared.runpod_client import RunPodClient
from datetime import datetime, timezone

def consume_stream():
    runpod_client = RunPodClient()
    consumer = RedisStreamConsumer(
        stream_name=settings.redis.streams.audio_upload_complete_remote,
        consumer_group=settings.runpod_trigger.consumer_group,
        consumer_name="consumer_1"
    )

    for entry_id, data in consumer.listen():
        logger.info(f"Processing {data}, entry: {entry_id}")
        try:
            s3_key = data['key']
            job_id = runpod_client.run_async({'key': s3_key}) 
            logger.info(f"Kicked off runpod job {job_id}")
            # Not being used now. For observability in the future
            consumer.client.xadd("runpod_jobs_fired", {
                "job_id": job_id,
                "s3_key": s3_key,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            consumer.ack(entry_id)
        except Exception as e:
            logger.error(f"❌ Failed to trigger runpod for {data.get('file')}: {str(e)}", exc_info=True)
