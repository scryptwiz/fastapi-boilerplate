"""Settings API endpoint for displaying application configuration"""

from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/")
def get_settings_info(request: Request):
    """Get current application settings (excluding sensitive data)"""
    settings = request.app.state.settings
    
    return {
        "application": {
            "name": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT.value,
        },
        "database": {
            "host": settings.POSTGRES_HOST,
            "port": settings.POSTGRES_PORT,
            "database": settings.POSTGRES_DB,
            "user": settings.POSTGRES_USER,
            "sync_url": settings.database_url_sync,
            "async_url": settings.database_url_async,
        },
        "redis": {
            "host": settings.REDIS_HOST,
            "port": settings.REDIS_PORT,
            "url": settings.redis_url,
        },
        "api": {
            "base_url": settings.API_BASE_URL,
            "log_level": settings.LOG_LEVEL.value,
        },
        "features": {
            "feature_x_enabled": settings.FEATURE_X_ENABLED,
        },
        "environment_flags": {
            "is_development": settings.is_development,
            "is_production": settings.is_production,
        }
    }

@router.get("/health")
def settings_health_check(request: Request):
    """Health check endpoint that uses settings"""
    settings = request.app.state.settings
    
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT.value,
        "database_configured": bool(settings.POSTGRES_URL),
        "redis_configured": bool(settings.REDIS_HOST),
        "app_version": settings.APP_VERSION,
    }

@router.get("/demo/environment-behavior")
def demo_environment_behavior(request: Request):
    """Demo endpoint showing environment-specific behavior"""
    settings = request.app.state.settings
    
    response = {
        "message": "Demo of environment-specific behavior",
        "environment": settings.ENVIRONMENT.value,
    }
    
    if settings.is_development:
        response.update({
            "debug_info": {
                "all_environment_variables": True,
                "detailed_logging": True,
                "mock_data_enabled": True,
                "database_url": settings.database_url_sync,
            },
            "development_features": {
                "hot_reload": True,
                "debug_toolbar": True,
                "test_data": ["sample1", "sample2", "sample3"]
            }
        })
    elif settings.is_production:
        response.update({
            "production_info": {
                "security_enabled": True,
                "caching_enabled": True,
                "monitoring_enabled": True,
            }
        })
    else:  # staging
        response.update({
            "staging_info": {
                "feature_flags_enabled": True,
                "integration_testing": True,
            }
        })
    
    return response

@router.get("/demo/feature-flags")
def demo_feature_flags(request: Request):
    """Demo endpoint showing feature flag usage"""
    settings = request.app.state.settings
    
    features = {
        "feature_x_enabled": settings.FEATURE_X_ENABLED,
        "environment": settings.ENVIRONMENT.value,
    }
    
    if settings.FEATURE_X_ENABLED:
        features["feature_x_data"] = {
            "status": "enabled",
            "description": "This feature is currently active",
            "capabilities": ["capability_1", "capability_2", "capability_3"]
        }
    else:
        features["feature_x_data"] = {
            "status": "disabled",
            "description": "This feature is currently inactive"
        }
    
    return features
