from contextlib import asynccontextmanager

from lms.config.settings import Settings


settings = Settings()

class AppUtility:
    # for lifespan of an app
    @staticmethod
    @asynccontextmanager
    async def create_lifespan(app) :
        print(f'Server is starting at port {settings.PORT}...')
        yield
        print(f'Server is shutting down..')



