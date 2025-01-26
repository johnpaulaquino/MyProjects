from redis.asyncio import Redis
import asyncio
import json
from datetime import date,datetime, timezone
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
            to_string = json.dumps(data)
            await redis_app.set(name=f'user:{email}', value=to_string)
            return True
        return False
    
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
        
        if not name:
            return False
        
        email = f'user:{name}'
        # get the data
        existing_user = await redis_app.get(name=email)
        # extract into dict
        to_json : dict = json.loads(existing_user)
        # update the token of existing data
        to_json.update({key:token})

        # set again the data
        await RedisUserCached.set_user_data(email, json.dumps(to_json))
        return True
    
    @staticmethod
    async def get_user_by_email(email: str):
        """
        This method is to get the specific data in the cache.
        :param email:
            is the hash key in the redis to get the data that corresponds in the email
        :return:
            the data of the specific user
        """
        user = await redis_app.get(f'user:{email}')
        to_json : dict = json.loads(user)
        return to_json


user_data = {
        "name": "John",
        "age" : 30,  # This will be converted to string in the method
        "city": "New York",
        'postal': 4009,
}


async def main():
    user = await RedisUserCached.get_user_by_email('123')
    print(user)
    await redis_app.hset('user',  mapping=user_data)
    print(await redis_app.hgetall('user'))

# print(asyncio.run(redis_app.flushall()))
# print(asyncio.run(RedisUserCached.set_user_data('123',user_data)))
# asyncio.run(main())
# print(asyncio.run(RedisUserCached.update_access_token('123', 'toekn', 'faketoken')))
