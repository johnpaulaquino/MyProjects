from fastapi import FastAPI
import uvicorn

title = 'E-LMS'
description = """
# 📖 E-Library Management System
"""
app = FastAPI(
        title=title,
        description=description,
        version='1.0'
)

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
