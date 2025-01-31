import uvicorn
from fastapi import FastAPI

from taskmanagement.utils.utility import Utility
from taskmanagement.routes.signup import signup
from taskmanagement.routes.auth import auth

description = """
# 📋 Task Management API
"""

app = FastAPI(
        version='1.0.0',
        summary="This is simple API, which handle a basic task management.",
        lifespan=Utility.lifespan,
        description=description)


app.include_router(signup)
app.include_router(auth)




if __name__ == '__main__':
    uvicorn.run('app:app',reload=True)