from fastapi import APIRouter, FastAPI

from app.api.v1 import api_v1_router
from app.core.config import Settings


api = APIRouter(prefix="/api")

api.include_router(api_v1_router)


def register_routers(app: FastAPI):
    """Register all API routers with the FastAPI application"""
    app.include_router(api)
    
    # Make settings accessible in request dependencies
    @app.middleware("http")
    async def add_settings_to_request(request, call_next):
        request.state.settings = app.state.settings
        request.state.db_manager = app.state.db_manager
        response = await call_next(request)
        return response
