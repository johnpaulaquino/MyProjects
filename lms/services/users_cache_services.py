from lms.services.redis_caching_app import redis_app, RedisError
from fastapi.encoders import jsonable_encoder
class UsersCacheServices:
    
    @staticmethod
    async def insert_user_cred(user_id : str, data : dict):
        try:
            if not isinstance(data, dict):
                return False
            string_data = jsonable_encoder(data)
            await redis_app.hset(name= f'user:{user_id}',mapping = string_data)
            return True
        except RedisError as e:
            print(f'An error occurred {e}')
    
    @staticmethod
    async def get_user_cred(user_id : str):
        try:
            if not user_id:
                return False
            
            return await redis_app.hgetall(name = f'user:{user_id}')
        except RedisError as e:
            print(f'An error occurred {e}')
            