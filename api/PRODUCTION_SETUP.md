# 🚀 Production Setup Guide

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r api/requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `api/.env`:

```bash
# Security
SECRET_KEY=your-secret-key-min-32-chars-change-in-production
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=30

# Database
DATABASE_PATH=ghostpen.db

# OpenAI
OPENAI_API_KEY=sk-proj-your-key-here

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
ENVIRONMENT=development

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10
```

### 3. Запуск API

```bash
cd api
python main.py
```

Или через uvicorn:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔐 Новые эндпоинты аутентификации

### Регистрация

```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "Иван Иванов",
  "password": "securepassword123"
}
```

**Ответ:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "uuid",
  "email": "user@example.com",
  "name": "Иван Иванов"
}
```

### Вход

```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Получить текущего пользователя

```bash
GET /api/auth/me
Authorization: Bearer <access_token>
```

## 📊 Улучшенный Health Check

```bash
GET /api/health
```

**Ответ:**
```json
{
  "status": "healthy",
  "version": "1.1.0",
  "environment": "development",
  "services": {
    "database": true,
    "generator": true,
    "profiler": true,
    "openai_configured": true
  }
}
```

## 📝 Логирование

Логи теперь в JSON формате (в production) или текстовом (в development).

Пример JSON лога:
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "api.main",
  "message": "User registered successfully",
  "user_id": "uuid",
  "module": "main",
  "function": "register",
  "line": 45
}
```

## 🔒 Безопасность

### CORS

В production обязательно укажите конкретные домены:

```bash
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### SECRET_KEY

**КРИТИЧНО**: В production используйте сильный SECRET_KEY (минимум 32 символа):

```bash
# Генерация секретного ключа
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Пароли

Пароли автоматически хэшируются с помощью bcrypt перед сохранением в БД.

## 🧪 Тестирование

### Регистрация и вход

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User","password":"test123456"}'

# Вход
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'

# Получить информацию о себе
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## 🚨 Важные замечания

1. **SECRET_KEY** должен быть уникальным и секретным
2. **ALLOWED_ORIGINS** не должен содержать `*` в production
3. **Пароли** минимум 6 символов
4. **Логи** содержат чувствительные данные - настройте ротацию и архивацию

## 📚 Дополнительная документация

- [PRODUCTION_READY.md](../PRODUCTION_READY.md) - полный чеклист production-ready
- [API Documentation](http://localhost:8000/docs) - Swagger UI после запуска

