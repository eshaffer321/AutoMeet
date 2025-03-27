import datetime
from shared.clients.redis_client import RedisStreamConsumer
from config.config import settings
from pony.orm import db_session
from shared.database import Recording

consumer = RedisStreamConsumer(
    stream_name=settings.redis.streams.transcription_complete,
    consumer_group=settings.metadata_indexer.consumer_group,
    consumer_name="consumer_1"
)

@db_session
def handler(data):
    s3_key_raw = data["key_raw"]
    s3_key_merged = data["merged_key"]
    id = data["id"]
    recording_ended_at = data["recording_ended_at"]
    recording_ended_at = datetime.fromisoformat(recording_ended_at.replace("Z", "+00:00"))
    Recording(
        id=id,
        s3_key_raw=s3_key_raw,
        s3_key_merged=s3_key_merged,
        recording_ended_at=recording_ended_at
    )

def consume_stream():
    consumer.process(handler_fn=handler)



