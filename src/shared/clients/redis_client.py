import redis
import time
from config.config import settings
from shared.util.logging import logger 


def get_redis_client():
    """Helper to initialize a new Redis client."""
    return redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        decode_responses=True,
        password=settings.redis.password,
        ssl=True
    )

class RedisStreamConsumer:
    def __init__(self, stream_name, consumer_group, consumer_name, block=0, count=1):
        self.stream_name = stream_name
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        self.block = block  # How long to block waiting for messages (0 = indefinitely)
        self.count = count  # How many messages to read at a time
        self.client = get_redis_client()

        # Ensure the consumer group exists
        try:
            self.client.xgroup_create(self.stream_name, self.consumer_group, id='$', mkstream=True)
        except redis.exceptions.ResponseError:
            # Likely means the group already exists
            pass

    def listen(self):
        """
        Generator that yields (entry_id, data) tuples from the stream.
        It automatically handles reconnection if the connection drops.
        """
        while True:
            try:
                logger.info(f"Waiting for messages from stream {self.stream_name}")
                messages = self.client.xreadgroup(
                    groupname=self.consumer_group,
                    consumername=self.consumer_name,
                    streams={self.stream_name: ">"},
                    count=self.count,
                    block=self.block
                )
                if messages:
                    for stream, entries in messages:
                        for entry_id, data in entries:
                            yield entry_id, data
            except ConnectionError as e:
                logger.error(f"Redis connection lost: {e}")
                logger.info("Reinitializing Redis client in 5 seconds...")
                time.sleep(5)
                self.client = get_redis_client()

    def process(self, handler_fn):
        """Process each message using the provided handler function."""
        for entry_id, data in self.listen():
            logger.info(f"🔄 Processing entry {entry_id} with data: {data}")
            try:
                handler_fn(data)
                self.ack(entry_id)
            except Exception as e:
                logger.error(f"❌ Error handling entry {entry_id}: {e}", exc_info=True)

    def ack(self, message_id):
        """Acknowledge the processing of a message."""
        self.client.xack(self.stream_name, self.consumer_group, message_id)