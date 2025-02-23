from fastapi import FastAPI
import uvicorn

from lms.config.settings import Settings
from lms.routes.signup import signup
from lms.routes.login import login

from lms.utils.app_utils import AppUtility

settings = Settings()

title = 'E-LMS'
description = """
# 📖 E-Library Management System
"""
app = FastAPI(
        title=title,
        description=description,
        version='1.0',
        lifespan=AppUtility.create_lifespan
)

app.include_router(signup)
app.include_router(login)

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
