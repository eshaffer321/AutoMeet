import redis
from config import settings

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=True
)