"""Dependencies for accessing application settings and services"""

from fastapi import Depends, Request
from app.core.config import Settings
from app.core.db.database import DatabaseManager, get_sync_db, get_async_db


def get_settings(request: Request) -> Settings:
    """FastAPI dependency to get application settings"""
    return request.app.state.settings


def get_db_manager(request: Request) -> DatabaseManager:
    """FastAPI dependency to get database manager"""
    return request.app.state.db_manager


# Re-export database dependencies for convenience
__all__ = [
    "get_settings",
    "get_db_manager", 
    "get_sync_db",
    "get_async_db"
]
