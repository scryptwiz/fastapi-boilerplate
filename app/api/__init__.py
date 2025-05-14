from fastapi import APIRouter, FastAPI

from app.api.v1 import api_v1_router


api = APIRouter(prefix="/api")

api.include_router(api_v1_router)


def register_routers(app: FastAPI):
    app.include_router(api)
