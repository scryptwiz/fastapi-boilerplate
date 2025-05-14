from fastapi import Request, status
from slowapi.errors import RateLimitExceeded
from app.core.response import error


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return error(
        status=status.HTTP_429_TOO_MANY_REQUESTS, message="Too many requests", data=None
    )
