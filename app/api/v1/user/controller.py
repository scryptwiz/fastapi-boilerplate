from fastapi import APIRouter, Request, status, Depends

from app.api.v1.user.dto import create_user_dto
from app.core.dependencies import get_settings
from app.core.config import Settings
from app.core.rate_limiter import limiter
from app.core.response import success


router = APIRouter()


users = [
    {"name": "John"},
    {"name": "Jane"},
    {"name": "Joe"},
]


@router.post("/")
@limiter.limit("1/minute")
def create_user(
    request: Request, 
    payload: create_user_dto,
    settings: Settings = Depends(get_settings)
):
    # Example of using settings in the controller
    return success(
        status=status.HTTP_201_CREATED,
        success=True,
        message=f"User registered successfully in {settings.ENVIRONMENT.value} environment",
        data={
            **payload.dict(),
            "app_version": settings.APP_VERSION,
            "feature_x_enabled": settings.FEATURE_X_ENABLED
        },
    )


@router.get("/")
def get_users(settings: Settings = Depends(get_settings)):
    return {
        "message": users,
        "environment": settings.ENVIRONMENT.value,
        "total_users": len(users)
    }


@router.get("/{user_id}")
def get_user(user_id: int, settings: Settings = Depends(get_settings)):
    if user_id >= len(users):
        return {
            "error": "User not found",
            "environment": settings.ENVIRONMENT.value
        }
    return {
        "message": users[user_id],
        "environment": settings.ENVIRONMENT.value
    }
