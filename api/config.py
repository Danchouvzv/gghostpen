#!/usr/bin/env python3
"""
Конфигурация для GhostPen API.

Валидация переменных окружения и настройки приложения.
"""

import os
from typing import List, Optional
from pydantic import Field, field_validator
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback для старых версий
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # API
    API_TITLE: str = "GhostPen API"
    API_VERSION: str = "1.1.0"
    API_DESCRIPTION: str = "API для генерации постов в авторском стиле"
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY",
        description="Секретный ключ для JWT"
    )
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        env="ALLOWED_ORIGINS",
        description="Разрешенные домены для CORS"
    ) 
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=1440,  # 24 часа
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=30,
        env="REFRESH_TOKEN_EXPIRE_DAYS"
    )
    
    # Database
    DATABASE_URL: Optional[str] = Field(
        default=None,
        env="DATABASE_URL",
        description="URL базы данных (для PostgreSQL в production)"
    )
    DATABASE_PATH: str = Field(
        default="ghostpen.db",
        env="DATABASE_PATH",
        description="Путь к SQLite базе (для dev)"
    )
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        env="OPENAI_API_KEY",
        description="OpenAI API ключ"
    )
    
    # Logging
    LOG_LEVEL: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    LOG_FORMAT: str = Field(
        default="json",
        env="LOG_FORMAT",
        description="Формат логов (json, text)"
    )
    
    # Environment
    ENVIRONMENT: str = Field(
        default="development",
        env="ENVIRONMENT",
        description="Окружение (development, staging, production)"
    )
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(
        default=True,
        env="RATE_LIMIT_ENABLED"
    )
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=10,
        env="RATE_LIMIT_PER_MINUTE"
    )
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        """Парсит ALLOWED_ORIGINS из строки или списка."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v, info):
        """Проверяет, что SECRET_KEY установлен и не дефолтный."""
        if v == "your-secret-key-change-in-production":
            # Проверяем ENVIRONMENT из info.data если доступно
            env = info.data.get("ENVIRONMENT", "development") if hasattr(info, 'data') else "development"
            if env == "production":
                raise ValueError("SECRET_KEY должен быть изменен в production!")
        if len(v) < 32:
            raise ValueError("SECRET_KEY должен быть минимум 32 символа")
        return v
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        """Проверяет валидность окружения."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT должен быть одним из: {', '.join(allowed)}")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Глобальный экземпляр настроек
settings = Settings()

