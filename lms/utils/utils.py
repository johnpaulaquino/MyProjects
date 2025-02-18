from contextlib import asynccontextmanager
from uuid import uuid4
from lms.schema_models.settings import Settings
settings = Settings()
class Utility:
    
    
    @staticmethod
    def generate_uuid() -> str:
        return str(uuid4())
    
    
    
    
    @staticmethod
    @asynccontextmanager
    async def create_lifespan(app):
        print(f'Server is starting at port {settings.PORT}...')
        yield
        print(f'Server is shutting down..')