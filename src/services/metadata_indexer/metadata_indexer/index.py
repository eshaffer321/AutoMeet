from shared.clients.redis_client import RedisStreamConsumer
from config.config import settings
from pony.orm import db_session
from shared.database import Recording

consumer = RedisStreamConsumer(
    stream_name=settings.redis.streams.transcription_complete,
    consumer_group=settings.metadata_indexer.consumer_group,
    consumer="consumer_1"
)

@db_session
def handler(data):
    
   
    pass

def consume_stream():
    consumer.process(handler_fn=handler)



