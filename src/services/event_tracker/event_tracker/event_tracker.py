from datetime import datetime
import threading
from shared.clients.redis_client import RedisStreamConsumer 
from config.config import settings
from shared.util.logging import logger
from shared.database.models import Event
from shared.database.client import SessionLocal

def handler(stream):
    consumer = RedisStreamConsumer(
        stream_name=stream,
        consumer_group="event_tracker",
        consumer_name="event_tracker_consumer",
    )
    for entry_id, data in consumer.listen():
        logger.info(f"Received message: {data}")
        session = SessionLocal()
        timestamp_ms = int(entry_id.split('-')[0])
        dt = datetime.fromtimestamp(timestamp_ms / 1000.0)

        try:
            event = Event(
                recording_id = data["id"],
                stream_name=stream,
                redis_id=entry_id,
                timestamp=dt,
                payload=data
            )
            session.add(event)
            session.commit()
            consumer.client.xack(stream, "event_tracker", entry_id)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to insert event into the database: {e}")


def consume_stream():
    threads = []
    for stream in settings.redis.streams:
        t = threading.Thread(target=handler, args=(stream,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    