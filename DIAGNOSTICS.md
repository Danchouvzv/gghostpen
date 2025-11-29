# 🔍 Диагностика подключения Frontend ↔ Backend

## ✅ Проверка конфигурации

### Frontend (services/api.ts)
- ✅ API URL: `http://localhost:8000` (правильно)
- ✅ Использует реальный API (не mock)
- ✅ Endpoint: `/api/generate`

### Backend (api/main.py)
- ✅ CORS настроен: `allow_origins=["*"]` (разрешает все источники)
- ✅ Порт: `8000`
- ✅ Endpoints работают

## 🧪 Тестирование подключения

### 1. Проверка Backend

```bash
curl http://localhost:8000/api/health
```

Должен вернуть: `{"status": "healthy", ...}`

### 2. Проверка CORS

```bash
curl -X OPTIONS http://localhost:8000/api/generate \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

Должны быть заголовки `Access-Control-Allow-Origin: *`

### 3. Тест генерации

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{
    "author_id": "person_01",
    "social_network": "linkedin",
    "topic": "Тест подключения"
  }'
```

### 4. Тест в браузере

Откройте консоль браузера (F12) на http://localhost:3000 и выполните:

```javascript
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

## 🔧 Возможные проблемы

### Проблема: CORS ошибка

**Решение**: Убедитесь, что в `api/main.py`:
```python
allow_origins=["*"]  # Для разработки
```

### Проблема: Backend не отвечает

**Решение**: 
1. Проверьте, что backend запущен: `curl http://localhost:8000/api/health`
2. Проверьте порт в `services/api.ts`

### Проблема: 404 Not Found

**Решение**: Проверьте URL в `services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

## ✅ Ожидаемое поведение

1. Frontend на http://localhost:3000
2. Backend на http://localhost:8000
3. При нажатии "Generate" запрос идет на `http://localhost:8000/api/generate`
4. Backend отвечает с CORS заголовками
5. Пост генерируется и отображается

## 🎯 Проверка в браузере

1. Откройте http://localhost:3000
2. Откройте DevTools (F12) → Network
3. Нажмите "Generate"
4. Проверьте запрос к `http://localhost:8000/api/generate`
5. Проверьте ответ (должен быть статус 200)

## 📋 Чеклист

- [ ] Backend запущен на порту 8000
- [ ] Frontend запущен на порту 3000
- [ ] CORS настроен правильно
- [ ] API URL правильный в `services/api.ts`
- [ ] Frontend использует `services/api.ts` (не mockApi)
- [ ] Нет ошибок в консоли браузера
- [ ] Запросы проходят успешно

