from redis.asyncio import Redis,RedisError
import asyncio
try:
    redis_app = Redis(port = 6379 , host = '127.0.0.1', decode_responses = True)

except RedisError as e:
    print(f'An error occurred {e}')



