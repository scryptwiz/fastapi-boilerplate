from enum import Enum
from typing import Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file"""
    
    # Application Settings - all from env
    APP_NAME: str = Field(description="Application name")
    APP_DESCRIPTION: Optional[str] = Field(description="Application description")
    APP_VERSION: str = Field(description="Application version")
    
    # Environment
    ENVIRONMENT: EnvironmentOption = Field(description="Environment type")
    
    # Database Settings - all from env
    POSTGRES_HOST: str = Field(description="PostgreSQL host")
    POSTGRES_PORT: int = Field(description="PostgreSQL port")
    POSTGRES_USER: str = Field(description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(description="PostgreSQL password")
    POSTGRES_DB: str = Field(description="PostgreSQL database name")
    POSTGRES_URL: str = Field(description="Full PostgreSQL connection URL")
    
    # Redis Settings - all from env
    REDIS_HOST: str = Field(description="Redis host")
    REDIS_PORT: int = Field(description="Redis port")
    
    # Logging Settings - from env
    LOG_LEVEL: LogLevel = Field(description="Logging level")
    
    # API Settings - from env
    API_BASE_URL: str = Field(description="API base URL")
    
    # Security Settings - from env
    SECRET_KEY: str = Field(description="Secret key for cryptographic operations")
    
    # Feature Flags - from env
    FEATURE_X_ENABLED: bool = Field(description="Enable feature X")
    
    # Email Settings - from env
    EMAIL_HOST: str = Field(description="Email SMTP host")
    EMAIL_PORT: int = Field(description="Email SMTP port")
    
    @computed_field
    @property
    def database_url_sync(self) -> str:
        """Synchronous database URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @computed_field
    @property
    def database_url_async(self) -> str:
        """Asynchronous database URL"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @computed_field
    @property
    def redis_url(self) -> str:
        """Redis connection URL"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    @computed_field
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT == EnvironmentOption.LOCAL
    
    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT == EnvironmentOption.PRODUCTION

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Tell Pydantic to read from environment variables
        env_prefix = ""  # No prefix, use exact variable names

# Create settings instance that will load from environment/env file
settings = Settings()