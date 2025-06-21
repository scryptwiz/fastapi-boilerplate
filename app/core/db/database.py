"""Database configuration and connection management"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import Settings

# Base class for all ORM models
Base = declarative_base()

class DatabaseManager:
    """Database connection manager using settings"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._sync_engine = None
        self._async_engine = None
        self._sync_session_factory = None
        self._async_session_factory = None
    
    @property
    def sync_engine(self):
        """Get or create synchronous database engine"""
        if self._sync_engine is None:
            self._sync_engine = create_engine(
                self.settings.database_url_sync,
                echo=self.settings.is_development,  # Log SQL queries in development
                pool_pre_ping=True,
                pool_recycle=3600,
            )
        return self._sync_engine
    
    @property
    def async_engine(self):
        """Get or create asynchronous database engine"""
        if self._async_engine is None:
            self._async_engine = create_async_engine(
                self.settings.database_url_async,
                echo=self.settings.is_development,  # Log SQL queries in development
                pool_pre_ping=True,
                pool_recycle=3600,
            )
        return self._async_engine
    
    @property
    def sync_session_factory(self):
        """Get or create synchronous session factory"""
        if self._sync_session_factory is None:
            self._sync_session_factory = sessionmaker(
                bind=self.sync_engine,
                autocommit=False,
                autoflush=False,
            )
        return self._sync_session_factory
    
    @property
    def async_session_factory(self):
        """Get or create asynchronous session factory"""
        if self._async_session_factory is None:
            self._async_session_factory = async_sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )
        return self._async_session_factory
    
    def get_sync_session(self):
        """Get a synchronous database session"""
        return self.sync_session_factory()
    
    def get_async_session(self):
        """Get an asynchronous database session"""
        return self.async_session_factory()
    
    async def create_tables(self):
        """Create all database tables"""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self):
        """Drop all database tables"""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

# Global database manager instance (will be initialized with settings)
db_manager: DatabaseManager = None

def initialize_database(settings: Settings) -> DatabaseManager:
    """Initialize the global database manager with settings"""
    global db_manager
    db_manager = DatabaseManager(settings)
    return db_manager

def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance"""
    if db_manager is None:
        raise RuntimeError("Database manager not initialized. Call initialize_database() first.")
    return db_manager

# Dependency for FastAPI to get database sessions
def get_sync_db():
    """FastAPI dependency for synchronous database sessions"""
    db = get_db_manager().get_sync_session()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """FastAPI dependency for asynchronous database sessions"""
    async with get_db_manager().get_async_session() as db:
        yield db