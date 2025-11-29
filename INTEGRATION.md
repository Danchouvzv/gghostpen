# 🔗 Интеграция GhostPen Backend + Frontend

Инструкция по подключению ML-бэкенда к фронтенду.

## 📋 Структура

```
ghostpen/                    # Backend (ML)
├── api/                     # FastAPI сервер
│   ├── main.py             # API эндпоинты
│   └── requirements.txt    # Зависимости
├── scripts/                 # ML компоненты
└── dataset/                 # Данные

ghostpenfrontend/            # Frontend (React)
├── services/
│   ├── api.ts              # Реальный API (новый)
│   └── mockApi.ts          # Mock API (для разработки)
└── App.tsx                 # Главный компонент
```

## 🚀 Быстрый старт

### 1. Запуск Backend

```bash
cd /Users/danialtalgatov/Documents/ghostpen

# Установка зависимостей
pip install -r api/requirements.txt

# Запуск сервера
cd api
python main.py

# Или через uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Сервер запустится на: http://localhost:8000

### 2. Запуск Frontend

```bash
cd /Users/danialtalgatov/Downloads/ghostpenfrontend

# Установка зависимостей (если еще не установлены)
npm install

# Запуск dev сервера
npm run dev
```

Frontend запустится на: http://localhost:5173 (или другой порт Vite)

### 3. Проверка подключения

1. Откройте http://localhost:8000/docs - документация API
2. Откройте http://localhost:8000/api/health - проверка здоровья
3. Откройте http://localhost:5173 - фронтенд

## 🔧 Конфигурация

### Backend

По умолчанию используется **mock LLM** (для тестирования).

Для реальной генерации через OpenAI:

```bash
export OPENAI_API_KEY="your-api-key"
```

Затем обновите `api/main.py`:
```python
import os
api_key = os.getenv("OPENAI_API_KEY")
generator = GhostPenGenerator(PROFILES_PATH, api_key)
```

### Frontend

В `services/api.ts` можно изменить URL бэкенда:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

Или создайте `.env` файл:
```
VITE_API_URL=http://localhost:8000
```

## 🔄 Переключение между Mock и Real API

### Использовать Real API (по умолчанию)

В `App.tsx`:
```typescript
import { generatePost } from './services/api';
```

### Использовать Mock API (для разработки)

В `App.tsx`:
```typescript
import { generatePost } from './services/mockApi';
```

## 📡 API Эндпоинты

### `POST /api/generate`

Генерация поста в стиле автора.

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

### `GET /api/authors`

Список доступных авторов.

### `GET /api/health`

Проверка здоровья сервиса.

## 🐛 Troubleshooting

### Backend не запускается

1. Проверьте, что установлены все зависимости:
   ```bash
   pip install -r api/requirements.txt
   ```

2. Проверьте, что файл профилей существует:
   ```bash
   ls dataset/author_profiles.json
   ```

3. Если профилей нет, сгенерируйте их:
   ```bash
   python scripts/style_profiler.py dataset/dataset.json dataset/author_profiles.json
   ```

### Frontend не подключается к Backend

1. Проверьте CORS настройки в `api/main.py`
2. Убедитесь, что backend запущен на порту 8000
3. Проверьте URL в `services/api.ts`

### Ошибки генерации

1. Проверьте логи backend в консоли
2. Убедитесь, что `author_id` существует в профилях
3. Проверьте формат `social_network` (linkedin, instagram, facebook, telegram)

## ✅ Чеклист готовности

- [ ] Backend запущен на http://localhost:8000
- [ ] Frontend запущен на http://localhost:5173
- [ ] Профили авторов сгенерированы (`author_profiles.json`)
- [ ] API отвечает на `/api/health`
- [ ] Frontend может делать запросы к `/api/generate`
- [ ] Генерация постов работает

## 🎯 Следующие шаги

1. **Добавить авторов в фронтенд**: Обновите `constants.ts` с реальными данными из `/api/authors`
2. **Настроить OpenAI**: Добавьте API ключ для реальной генерации
3. **Оптимизация**: Добавьте кэширование, rate limiting
4. **Мониторинг**: Добавьте логирование и метрики

