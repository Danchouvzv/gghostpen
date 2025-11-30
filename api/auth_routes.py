#!/usr/bin/env python3
"""
Auth routes для GhostPen API.

Эндпоинты для регистрации, логина и управления токенами.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid

from database import Database
from auth import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    get_current_user,
    decode_token
)

try:
    from logger import get_logger
    logger = get_logger(__name__)
except:
    import logging
    logger = logging.getLogger(__name__)

# get_db будет импортирован позже, чтобы избежать circular import
# Используем функцию-заглушку, которая будет заменена в main.py
def get_db():
    """Dependency для Database - будет переопределена в main.py."""
    return Database()

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Database = Depends(lambda: get_db())):
    """Регистрация нового пользователя."""
    logger.info(f"Registration attempt for email: {request.email}")
    
    # Проверяем, существует ли пользователь
    existing_user = db.get_user_by_email(request.email)
    if existing_user:
        logger.warning(f"Registration failed: email already exists - {request.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создаем пользователя
    user_id = str(uuid.uuid4())
    password_hash = get_password_hash(request.password)
    
    success = db.create_user(
        user_id=user_id,
        email=request.email,
        name=request.name,
        password_hash=password_hash
    )
    
    if not success:
        logger.error(f"Failed to create user: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания пользователя"
        )
    
    logger.info(f"User registered successfully: {user_id}")
    
    # Создаем токены
    token_data = {"sub": user_id, "email": request.email, "name": request.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id,
        email=request.email,
        name=request.name
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Database = Depends(lambda: get_db())):
    """Вход пользователя."""
    logger.info(f"Login attempt for email: {request.email}")
    
    # Получаем пользователя
    user = db.get_user_by_email(request.email)
    if not user:
        logger.warning(f"Login failed: user not found - {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Проверяем пароль
    password_hash = user.get("password_hash")
    if not password_hash or not verify_password(request.password, password_hash):
        logger.warning(f"Login failed: invalid password - {request.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    logger.info(f"User logged in successfully: {user['id']}")
    
    # Создаем токены
    token_data = {
        "sub": user["id"],
        "email": user.get("email"),
        "name": user.get("name")
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user["id"],
        email=user.get("email"),
        name=user.get("name")
    )


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Получить информацию о текущем пользователе."""
    return {
        "user_id": current_user["user_id"],
        "email": current_user.get("email"),
        "name": current_user.get("name")
    }


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest):
    """Обновить access token используя refresh token."""
    logger.info("Refresh token request")
    
    # Декодируем refresh token
    payload = decode_token(request.refresh_token)
    
    if payload is None:
        logger.warning("Invalid refresh token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный refresh token"
        )
    
    # Проверяем тип токена
    if payload.get("type") != "refresh":
        logger.warning("Wrong token type for refresh")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не является refresh token"
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не содержит user_id"
        )
    
    # Получаем пользователя из БД для актуальных данных
    db = get_db()
    user = db.get_user(user_id)
    if not user:
        logger.warning(f"User not found for refresh: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    logger.info(f"Token refreshed for user: {user_id}")
    
    # Создаём новые токены
    token_data = {
        "sub": user_id,
        "email": user.get("email"),
        "name": user.get("name")
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id,
        email=user.get("email"),
        name=user.get("name")
    )

