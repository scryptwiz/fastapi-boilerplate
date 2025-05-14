from fastapi import APIRouter, Request, status

from app.api.v1.user.dto import create_user_dto
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
def create_user(request: Request, payload: create_user_dto):
    return success(
        status=status.HTTP_201_CREATED,
        success=True,
        message="User Registered successfully",
        data=payload,
    )


@router.get("/")
def get_users():
    return {"message": users}


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": users[user_id]}
