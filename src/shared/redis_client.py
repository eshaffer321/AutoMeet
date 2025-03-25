import redis
from config.config import settings

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    decode_responses=True,
    password=settings.redis.password,
    ssl=True
)