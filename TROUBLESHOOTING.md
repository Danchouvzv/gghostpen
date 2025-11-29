# 🔧 Решение проблем подключения

## ❌ Ошибка: `ERR_CONNECTION_REFUSED`

Эта ошибка означает, что **backend не запущен** или недоступен.

### ✅ Решение:

1. **Проверьте, запущен ли backend:**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Если не запущен, запустите:**
   ```bash
   cd /Users/danialtalgatov/Documents/ghostpen/api
   export OPENAI_API_KEY="sk-proj-..."
   python3 main.py
   ```

3. **Или используйте скрипт:**
   ```bash
   cd /Users/danialtalgatov/Documents/ghostpen
   ./start_backend.sh
   ```

### 🔍 Диагностика:

#### Проверка порта:
```bash
lsof -ti:8000
```
Если команда ничего не выводит — порт свободен (backend не запущен).

#### Проверка backend:
```bash
curl http://localhost:8000/api/health
```
Должен вернуть: `{"status": "healthy", ...}`

#### Проверка авторов:
```bash
curl http://localhost:8000/api/authors
```
Должен вернуть массив авторов.

### 🚀 Быстрый запуск обоих сервисов:

**Терминал 1 (Backend):**
```bash
cd /Users/danialtalgatov/Documents/ghostpen/api
export OPENAI_API_KEY="sk-proj-..."
python3 main.py
```

**Терминал 2 (Frontend):**
```bash
cd /Users/danialtalgatov/Downloads/ghostpenfrontend
npm run dev
```

### ⚠️ Частые проблемы:

1. **Backend остановился:**
   - Проверьте логи на ошибки
   - Убедитесь, что порт 8000 свободен
   - Перезапустите backend

2. **CORS ошибки:**
   - Backend уже настроен с `allow_origins=["*"]`
   - Если проблема остаётся, проверьте URL в `api.ts`

3. **Frontend не может подключиться:**
   - Убедитесь, что backend запущен
   - Проверьте URL: `http://localhost:8000`
   - Откройте DevTools → Network для диагностики

### 📊 Проверка статуса:

```bash
# Backend
curl http://localhost:8000/api/health

# Frontend
curl http://localhost:5173
```

### ✅ Если всё работает:

- Backend: `http://localhost:8000` → `{"status": "healthy"}`
- Frontend: `http://localhost:5173` → открывается в браузере
- API: `http://localhost:8000/api/authors` → возвращает авторов

