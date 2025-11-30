#!/usr/bin/env python3
"""
Утилита для проверки API ключей GhostPen.

Показывает статус всех необходимых API ключей и переменных окружения.
"""

import os
import sys
from pathlib import Path

# Загружаем .env если есть
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Загружен .env файл: {env_path}")
    else:
        print(f"⚠️  .env файл не найден: {env_path}")
        print("   Используются системные переменные окружения")
except ImportError:
    print("⚠️  python-dotenv не установлен, используем системные переменные")

print("\n" + "="*60)
print("🔑 Проверка API ключей GhostPen")
print("="*60 + "\n")

# Проверяем SECRET_KEY
secret_key = os.getenv("SECRET_KEY")
if secret_key:
    if len(secret_key) >= 32:
        masked = secret_key[:8] + "..." + secret_key[-4:] if len(secret_key) > 12 else "***"
        print(f"✅ SECRET_KEY: {masked} (длина: {len(secret_key)})")
    else:
        print(f"⚠️  SECRET_KEY слишком короткий: {len(secret_key)} символов (нужно минимум 32)")
else:
    print("❌ SECRET_KEY не установлен")

# Проверяем OPENAI_API_KEY
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    masked = openai_key[:8] + "..." + openai_key[-4:] if len(openai_key) > 12 else "***"
    print(f"✅ OPENAI_API_KEY: {masked} (длина: {len(openai_key)})")
    
    # Проверяем формат
    if openai_key.startswith("sk-"):
        print("   ✅ Формат ключа корректный (начинается с sk-)")
    else:
        print("   ⚠️  Необычный формат ключа (обычно начинается с sk-)")
else:
    print("❌ OPENAI_API_KEY не установлен")
    print("   ⚠️  Будет использоваться mock генерация")

# Проверяем другие важные переменные
print("\n📋 Другие переменные окружения:")
print("-" * 60)

variables = {
    "DATABASE_PATH": os.getenv("DATABASE_PATH", "ghostpen.db (default)"),
    "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS", "не установлено"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO (default)"),
    "ENVIRONMENT": os.getenv("ENVIRONMENT", "development (default)"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440 (default)"),
}

for key, value in variables.items():
    status = "✅" if value != "не установлено" else "⚠️"
    print(f"{status} {key}: {value}")

# Генерируем пример SECRET_KEY если его нет
print("\n" + "="*60)
if not secret_key or len(secret_key) < 32:
    print("🔧 Генерация нового SECRET_KEY:")
    print("-" * 60)
    try:
        import secrets
        new_secret = secrets.token_urlsafe(32)
        print(f"SECRET_KEY={new_secret}")
        print("\n💡 Скопируйте эту строку в ваш .env файл")
    except ImportError:
        print("⚠️  Модуль secrets недоступен, используйте:")
        print("   python -c \"import secrets; print(secrets.token_urlsafe(32))\"")
else:
    print("✅ Все ключи настроены корректно!")

print("\n" + "="*60)
print("📝 Для настройки создайте файл api/.env с содержимым:")
print("-" * 60)
print("SECRET_KEY=your-secret-key-min-32-chars")
print("OPENAI_API_KEY=sk-proj-your-key-here")
print("DATABASE_PATH=ghostpen.db")
print("ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000")
print("LOG_LEVEL=INFO")
print("ENVIRONMENT=development")
print("="*60)

