from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded

from app.api import register_routers
from app.core import limiter, LogLevels, configure_logging, rate_limit_exceeded_handler, validation_exception_handler, internal_server_error_handler

app = FastAPI()

# Logger Initiation
configure_logging(log_level=LogLevels.debug, log_to_file=True)

# Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Custom validation error handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Error 500 handler
app.add_exception_handler(500, internal_server_error_handler)


@app.get("/")
def root():
    return "kelvin is a top tier swe and probably debugging this server rn. 🚀"


register_routers(app)
