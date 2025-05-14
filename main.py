from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded

from app.api import register_routers
from app.core.exception_handler import rate_limit_exceeded_handler
from app.core.logging import LogLevels, configure_logging
from app.core.rate_limiter import limiter
from app.core.response import error

app = FastAPI()

# Logger Initiation
configure_logging(log_level=LogLevels.debug, log_to_file=True)

# Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# Custom validation error handler
@app.exception_handler(RequestValidationError)
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


# Error 500 handler
@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return error(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        success=False,
        message="OOPS! Something went wrong",
        data=None,
    )


@app.get("/")
def root():
    return {"message": "Kelvin Is A Good Boy!"}


register_routers(app)
