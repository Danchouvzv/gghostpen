# 🚀 GhostPen API

FastAPI backend для GhostPen — генерация постов в авторском стиле.

## 📋 Быстрый старт

### 1. Установка зависимостей

```bash
cd api
pip install -r requirements.txt
```

### 2. Запуск сервера

```bash
# Разработка
python main.py

# Или через uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Документация API

После запуска откройте:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 Эндпоинты

### `GET /`
Информация о сервисе

### `GET /api/health`
Проверка здоровья сервиса

### `GET /api/authors`
Получить список доступных авторов

**Ответ:**
```json
{
  "authors": [
    {
      "id": "person_01",
      "name": "Person 01",
      "total_posts": 5,
      "platforms": ["linkedin", "facebook"],
      "stats": {
        "formality": "formal",
        "avgLength": 300,
        "emojiDensity": "Low"
      }
    }
  ]
}
```

### `POST /api/generate`
Генерация поста в стиле автора

**Запрос:**
```json
{
  "author_id": "person_01",
  "social_network": "linkedin",
  "topic": "О важности планирования",
  "sample_posts": []
}
```

**Ответ:**
```json
{
  "generated_post": "Сегодня хочу поделиться мыслями...",
  "style_similarity": 0.85,
  "debug": {
    "target_length": 300,
    "model_version": "ghostpen-v1.0",
    "processing_time_ms": 1450,
    "prompt_tokens": 342
  }
}
```

## 🔧 Конфигурация

### Использование OpenAI API

Для реальной генерации через OpenAI:

```bash
export OPENAI_API_KEY="your-api-key"
```

Затем обновите `main.py`:
```python
api_key = os.getenv("OPENAI_API_KEY")
generator = GhostPenGenerator(PROFILES_PATH, api_key)
```

### Без API ключа

По умолчанию используется mock-генератор для тестирования.

## 🌐 CORS

API настроен для работы с фронтендом. В продакшене обновите `allow_origins`:

```python
allow_origins=["http://localhost:5173", "https://yourdomain.com"]
```

## 📊 Структура

```
api/
├── main.py              # FastAPI приложение
├── requirements.txt     # Зависимости
└── README.md           # Эта документация
```

## 🧪 Тестирование

```bash
# Проверка здоровья
curl http://localhost:8000/api/health

# Список авторов
curl http://localhost:8000/api/authors

# Генерация поста
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "author_id": "person_01",
    "social_network": "linkedin",
    "topic": "О важности планирования"
  }'
```

