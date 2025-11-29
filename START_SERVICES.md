# 🚀 Запуск сервисов GhostPen

## ✅ Сервисы запущены!

### 🔧 Backend
- **URL:** http://localhost:8000
- **Health:** http://localhost:8000/api/health
- **API Docs:** http://localhost:8000/docs
- **Логи:** `/tmp/ghostpen_backend.log`

### 🎨 Frontend
- **URL:** http://localhost:5173
- **Логи:** `/tmp/ghostpen_frontend.log`

---

## 📝 Команды для запуска

### Backend:
```bash
cd /Users/danialtalgatov/Documents/ghostpen/api
export OPENAI_API_KEY="sk-proj-..."
python3 main.py
```

### Frontend:
```bash
cd /Users/danialtalgatov/Downloads/ghostpenfrontend
npm run dev
```

---

## 🔍 Проверка статуса

### Backend:
```bash
curl http://localhost:8000/api/health
```

### Frontend:
```bash
curl http://localhost:5173
```

---

## 🛑 Остановка

### Backend:
```bash
kill $(lsof -ti:8000)
```

### Frontend:
```bash
kill $(lsof -ti:5173)
```

---

## 📊 Текущий статус

- ✅ Backend: запущен
- ✅ Frontend: запущен
- ✅ OpenAI API: настроен
- ✅ Авторы: 10 (7 казахских + 3 русских)

