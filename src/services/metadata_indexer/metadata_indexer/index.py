from datetime import datetime
from shared.database.client import SessionLocal
from shared.database.models import Recording
from shared.clients.redis_client import RedisStreamConsumer
from config.config import settings
from shared.util.logging import logger

# Initialize the Redis stream consumer
consumer = RedisStreamConsumer(
    stream_name=settings.redis.streams.transcription_complete,
    consumer_group=settings.metadata_indexer.consumer_group,
    consumer_name="consumer_1"
)

def handler(data):
    s3_key_raw = data["key_raw"]
    s3_key_merged = data["merged_key"]
    recording_id = data["id"]
    duration = round(float(data["duration"]))
    # Convert the ISO formatted string to a datetime object
    recording_ended_at = datetime.fromisoformat(data["recording_ended_at"].replace("Z", "+00:00"))
    
    session = SessionLocal()
    try:
        # Create a new Recording instance using the SQLAlchemy model
        new_recording = Recording(
            id=recording_id,
            s3_key_raw=s3_key_raw,
            s3_key_merged=s3_key_merged,
            recording_ended_at=recording_ended_at,
            duration=duration
        )
        # Add and commit the new instance to the database
        session.add(new_recording)
        session.commit()
        logger.info(f"✅ Successfully inserted recording {recording_id} into the database")

        consumer.client.xadd(settings.redis.streams.recordings_inserted, {
            "id": recording_id,
            "s3_key_raw": s3_key_raw,
            "s3_key_merged": s3_key_merged,
            "recording_ended_at": recording_ended_at.isoformat(),
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        session.rollback()  # Roll back the transaction if any error occurs
        logger.error(f"❌ Failed to insert recording {recording_id} into the database. Error: {e}")
    finally:
        session.close()  # Always close the session

def consume_stream():
    consumer.process(handler_fn=handler)