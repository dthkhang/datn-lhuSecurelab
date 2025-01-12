# security/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Gọi handler tiếp theo và nhận về response
        response: Response = await call_next(request)
        # Thêm header X-XSS-Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Thêm header X-Content-Type-Options
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        return response

