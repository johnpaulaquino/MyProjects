
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
import asyncio
import json
from datetime import date,datetime, timezone, timedelta

#This is to create a connection in my local redis
redis_app = Redis(
        host='127.0.0.1', #This is the localhost and it is default.
        port=6379, #This is the port and it is default.
        decode_responses=True, #To return the data as expected not in a byte type.
        auto_close_connection_pool=True) # To make the connection auto close after query.


class RedisUserCached:
    @staticmethod
    async def set_user_data(email: str, data: dict):
        """
        This method is for adding the data in a cache.
        :param email:
            is for the name of the hash and to make it unique.
        :param data:
            is the data to be inserted in the cache.
        :return:
            True after adding.
        """
        if not email:
            return False
        if data and isinstance(data, dict):
            await redis_app.set(name=f'user:{email}', value=json.dumps(data))
            return True
        return False
    
    @staticmethod
    async def set_user_code_verification(code : str, email : str):
        expiration = timedelta(minutes=1)
        await redis_app.set(name=f'verify_code:{email}',value=code,ex=int(expiration.total_seconds()))
        
    
    @staticmethod
    async def get_user_code_verification(email : str):
        existing_code = await redis_app.get(f'verify_code:{email}')
        
        if not existing_code:
            return False
    
        
        return existing_code
    
    @staticmethod
    async def update_access_token(name: str, key : str, token):
        """
        This method is to update the data in the cache
        :param name:
            is the hash name in redis, so this must be unique.
        :param key:
            is the one who need to update, and update the data if it is exists,
            otherwise add in the existing data.
        :param token:
            is the token after the user will log in.
        :return:
            True after updating.
        """
        
        if not name or not key:
            return False
        
        await redis_app.hset(name=f'user:{name}',key=key, value=token)
        return True
    
    @staticmethod
    async def get_user_by_email(email: str):
        existing_user = await redis_app.get(name=f'user:{email}')
        
        if not existing_user:
            return False
        
        user_data = json.loads(existing_user)  # Convert JSON string back to Python dictionary
        return user_data
    

user_data = {
        "name": "John",
        "age" : 30,  # This will be converted to string in the method
        "city": "New York",
        'postal': 4009,
        'date': date.today(),
}
address = {
        'postal':12,
        'city' : 'laguna'
        
}
async def main():
    new_data = jsonable_encoder(user_data)
    await redis_app.hset('hey',mapping=new_data)
    user = await redis_app.hgetall('hey')

    
    # # new_user = await RedisUserCached.get_user_by_email(user['email'])
    # # print(new_user)
    # await redis_app.hset('user',  mapping=user_data)
    # print(await redis_app.hgetall('user'))


# asyncio.run(RedisUserCached.set_user_code_verification('1234', 'hacker2'))
# print(asyncio.run(RedisUserCached.get_user_code_verification('hacker2')))
# print(asyncio.run(redis_app.ttl('verify_code:hacker2')))
# asyncio.run(RedisUserCached.set_user_data('hey',user_data))
# print(asyncio.run(main()))
# print(asyncio.run(RedisUserCached.get_user_by_email(email)))
# asyncio.run(redis_app.set('123',value=json.dumps(user_data)))
# print(asyncio.run(redis_app.get('123')))
# print(asyncio.run(redis_app.ping()))
# print(asyncio.run(redis_app.flushall()))
# print(asyncio.run(RedisUserCached.set_user_data('123',user_data)))
# print(asyncio.run(RedisUserCached.get_user_code_verification('pauljohn.app2024@gmail.com')))
# print(asyncio.run(RedisUserCached.get_user_by_email('hey')))
# print(asyncio.run(RedisUserCached.update_access_token('123', 'toekn', 'faketoken')))


