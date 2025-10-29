from contextvars import ContextVar
from typing import Awaitable, Callable
from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

current_request: ContextVar[Request | None ] = ContextVar('request_context', default=None)

class GlobalContextRequestMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        token = current_request.set(request)
        try:
            response = await call_next(request)
            return response
        finally:
            current_request.reset(token)