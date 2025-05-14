from fastapi import APIRouter

from app.api.v1.user.controller import router as users_router


api_v1_router = APIRouter(prefix="/v1")


api_v1_router.include_router(users_router, prefix="/users", tags=["users"])
