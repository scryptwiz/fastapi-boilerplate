from typing import Any
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


def response(status: int, success: bool, message: str, data: Any = None):
    # Convert Pydantic models to dict for JSON serialization
    if isinstance(data, BaseModel):
        data = data.model_dump()
    return {
        "status": status,
        "success": success,
        "message": message,
        "data": data,
    }


def success(
    status: int = status.HTTP_200_OK,
    success: bool = True,
    message: str = "Request Successful",
    data: Any = {},
):
    return JSONResponse(
        status_code=status, content=response(status, success, message, data)
    )


def error(
    status: int = status.HTTP_400_BAD_REQUEST,
    success: bool = False,
    message: str = "Request Failed",
    data: Any = {},
):
    return JSONResponse(
        status_code=status, content=response(status, success, message, data)
    )
