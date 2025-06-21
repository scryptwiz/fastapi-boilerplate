# FastAPI Demo - Settings Integration

This FastAPI application demonstrates proper settings integration using `pydantic-settings` for configuration management.

## Features

- ✅ Environment-based configuration
- ✅ Type-safe settings with Pydantic
- ✅ Database integration with settings
- ✅ Settings dependency injection
- ✅ Environment-specific behavior
- ✅ Computed fields for derived values

## Configuration

### Environment Variables

The application loads **all configuration from environment variables**. You must set them in a `.env` file or as system environment variables. No defaults are hardcoded in the Python code.

#### Application Settings

- `APP_NAME`: Application name
- `APP_DESCRIPTION`: Application description
- `APP_VERSION`: Application version
- `ENVIRONMENT`: Environment type (local/staging/production)

#### Database Settings

- `POSTGRES_HOST`: PostgreSQL host
- `POSTGRES_PORT`: PostgreSQL port
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name
- `POSTGRES_URL`: Full PostgreSQL connection URL (required - must be set in .env)

#### Redis Settings

- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port

#### Other Settings

- `LOG_LEVEL`: Logging level (debug/info/warning/error)
- `API_BASE_URL`: API base URL
- `SECRET_KEY`: Secret key for cryptographic operations (required - must be set in .env)
- `FEATURE_X_ENABLED`: Feature flag example (true/false)
- `EMAIL_HOST`: Email SMTP host
- `EMAIL_PORT`: Email SMTP port

### Environment Files

Create different `.env` files for different environments:

- `.env` - Local development (current)
- `.env.staging.example` - Staging environment template
- `.env.production.example` - Production environment template

## Usage

### Accessing Settings in Controllers

```python
from fastapi import Depends
from app.core.dependencies import get_settings
from app.core.config import Settings

@router.get("/example")
def example_endpoint(settings: Settings = Depends(get_settings)):
    return {
        "environment": settings.ENVIRONMENT.value,
        "app_name": settings.APP_NAME,
        "feature_enabled": settings.FEATURE_X_ENABLED
    }
```

### Database Integration

The database manager is automatically initialized with settings:

```python
from fastapi import Depends
from app.core.dependencies import get_db_manager, get_sync_db
from app.core.db.database import DatabaseManager

@router.get("/db-info")
def db_info(db_manager: DatabaseManager = Depends(get_db_manager)):
    return {
        "sync_url": db_manager.settings.database_url_sync,
        "async_url": db_manager.settings.database_url_async
    }
```

### Computed Fields

The settings class includes computed fields for commonly used derived values:

- `database_url_sync`: Synchronous PostgreSQL URL
- `database_url_async`: Asynchronous PostgreSQL URL
- `redis_url`: Redis connection URL
- `is_development`: True if environment is "local"
- `is_production`: True if environment is "production"

## Running the Application

1. Copy `.env.example` to `.env` and update values
2. Install dependencies: `pip install -r requirements.txt`
3. Start the server: `uvicorn main:app --reload`

## API Endpoints

- `GET /` - Root endpoint with app info
- `GET /health` - Health check with environment info
- `GET /docs` - Interactive API documentation
- `GET /api/v1/users/` - List users (with settings info)
- `POST /api/v1/users/` - Create user (with settings integration)

## Development vs Production

The application automatically adjusts behavior based on the `ENVIRONMENT` setting:

- **Development** (`local`):

  - Debug logging enabled
  - SQL query logging enabled
  - Detailed error responses

- **Production** (`production`):
  - Info level logging
  - SQL query logging disabled
  - Minimal error responses

## Security Notes

- Never commit `.env` files with real credentials
- Use strong `SECRET_KEY` values in production
- Use environment-specific database credentials
- Enable HTTPS in production environments

## Production Deployment

### Files to Exclude from Production

The following development/debug utilities should **NOT** be deployed to production:

- `show_settings.py` - Development tool for viewing settings
- `test_env_config.py` - Environment configuration demo
- `check_production.py` - Production readiness checker

These files are already added to `.gitignore` to prevent accidental commits.

### Production Readiness Check

Before deploying, run the production readiness check:

```bash
python check_production.py
```

This will warn you if any development files are present that shouldn't be in production.

### Deployment Best Practices

1. **Use environment-specific `.env` files**:

   - Copy `.env.production.example` to `.env` for production
   - Set real database URLs, secret keys, and API endpoints

2. **Exclude development files**:

   - Ensure development utilities are not included in production builds
   - Use `.gitignore` patterns to prevent accidental inclusion

3. **Environment variables priority**:
   - System environment variables override `.env` file values
   - Use container environment variables for sensitive data in production
