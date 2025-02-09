

from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request, status
from starlette.responses import JSONResponse


class AppMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, callable_next):
        try:
            response = await callable_next(request)
            return response
        except Exception as e:
            return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content=f'An error occurred {e}!'
            )
