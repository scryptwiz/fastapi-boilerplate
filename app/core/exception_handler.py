from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from app.core.response import error


# Rate limit exception handler
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return error(
        status=status.HTTP_429_TOO_MANY_REQUESTS, message="Too many requests", data=None
    )


# Validation exception handler
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = {}

    for error_detail in exc.errors():
        # Get the field name from loc
        # loc can be a tuple like ('body', 'field_name') or just ('field_name',)
        field_name_parts = error_detail.get("loc", [])
        field_name = str(field_name_parts[-1]) if field_name_parts else "unknown_field"

        message = error_detail.get("msg", "Unknown validation error")

        # Append message if multiple errors for the same field
        if field_name in formatted_errors:
            formatted_errors[field_name] += f"; {message}"
        else:
            formatted_errors[field_name] = message

    return error(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        success=False,
        message="Validation Failed",
        data={"details": formatted_errors},
    )


# Internal server error exception handler
async def internal_server_error_handler(request: Request, exc: Exception):
    return error(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        success=False,
        message="OOPS! Something went wrong",
        data=None,
    )
