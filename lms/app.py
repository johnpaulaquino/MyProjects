from fastapi import FastAPI
import uvicorn

from lms.utils.utils import Utility

title = 'E-LMS'
description = """
# 📖 E-Library Management System
"""
app = FastAPI(
        title=title,
        description=description,
        version='1.0',
        lifespan=Utility.create_lifespan
)


app.include_router()



if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
