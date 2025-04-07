from shared.util.logging import logger
from config.config import settings
from shared.clients.redis_client import RedisStreamConsumer
from shared.clients.runpod_client import RunPodClient
from datetime import datetime, timezone

runpod_client = RunPodClient()
consumer = RedisStreamConsumer(
    stream_name=settings.redis.streams.audio_upload_complete_remote,
    consumer_group=settings.runpod_trigger.consumer_group,
    consumer_name="consumer_1"
)

def handler(data):
    s3_key = data['key']
    id = data['id']
    recording_ended_at = data['recording_ended_at']
    job_id = runpod_client.run_async({'key': s3_key, 'id': id, 'recording_ended_at': recording_ended_at}) 
    logger.info(f"Kicked off runpod job {job_id}")
    # Not being used now. For observability in the future
    consumer.client.xadd(settings.redis.streams.runpod_jobs_fired, {
        "job_id": job_id,
        "id": id,
        "recording_ended_at": recording_ended_at,
        "s3_key": s3_key,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

def consume_stream():
    consumer.process(handler_fn=handler)
    