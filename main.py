from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded

from app.api import register_routers
from app.core.config import Settings
from app.core.db.database import initialize_database
from app.core.logging import configure_logging, LogLevels
from app.core.exception_handler import (
    rate_limit_exceeded_handler,
    validation_exception_handler,
    internal_server_error_handler,
)
from app.core.rate_limiter import limiter

# Initialize settings
settings = Settings()

# Create FastAPI app with settings
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.is_development,
)

# Make settings available throughout the app
app.state.settings = settings

# Initialize database with settings
db_manager = initialize_database(settings)
app.state.db_manager = db_manager

# Logger Initiation - use settings for log level
log_level = LogLevels.debug if settings.is_development else LogLevels.info
configure_logging(log_level=log_level, log_to_file=True)

# Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Custom validation error handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Error 500 handler
app.add_exception_handler(500, internal_server_error_handler)


@app.get("/")
def root():
    return {
        "message": "kelvin is a top tier swe and probably debugging this server rn. 🚀",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT.value,
        "feature_x_enabled": settings.FEATURE_X_ENABLED
    }


@app.get("/health")
def health_check():
    """Health check endpoint with settings info"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT.value,
        "version": settings.APP_VERSION,
        "database_connected": False,  # TODO: Add actual database health check
    }


register_routers(app)
