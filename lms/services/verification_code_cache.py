from lms.services.redis_caching_app import redis_app


class VerificationCache :
    @staticmethod
    async def store_otp(email: str , code: str , expiration) :
        await redis_app.set(name = f'code:{email}' , value = code , ex = expiration)
        return True
    
    @staticmethod
    async def retrieve_otp(email: str) :
        return await redis_app.get(name = f'code:{email}')
    
    @staticmethod
    async def delete_otp(email: str) :
        return await redis_app.delete(f'code:{email}')