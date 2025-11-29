# 🚀 Запуск GhostPen

## Быстрый запуск

### Вариант 1: Через скрипты (рекомендуется)

**Терминал 1 - Backend:**
```bash
cd /Users/danialtalgatov/Documents/ghostpen
./start_backend.sh
```

**Терминал 2 - Frontend:**
```bash
cd /Users/danialtalgatov/Downloads/ghostpenfrontend
./start_frontend.sh
```

### Вариант 2: Вручную

**Backend:**
```bash
cd /Users/danialtalgatov/Documents/ghostpen/api
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd /Users/danialtalgatov/Downloads/ghostpenfrontend
npm install
npm run dev
```

## Проверка

После запуска откройте в браузере:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Что должно работать

1. ✅ Backend отвечает на http://localhost:8000
2. ✅ Frontend открывается на http://localhost:5173
3. ✅ Можно выбрать автора, платформу и тему
4. ✅ Генерация постов работает
5. ✅ Результаты отображаются в интерфейсе

## Troubleshooting

### Backend не запускается

```bash
# Проверьте зависимости
pip install -r api/requirements.txt

# Проверьте профили
ls dataset/author_profiles.json

# Если профилей нет:
python scripts/style_profiler.py dataset/dataset.json dataset/author_profiles.json
```

### Frontend не запускается

```bash
# Установите зависимости
npm install

# Проверьте, что порт 5173 свободен
lsof -ti:5173
```

### CORS ошибки

Убедитесь, что в `api/main.py` настроен CORS:
```python
allow_origins=["*"]  # Для разработки
```

## Готово! 🎉

Теперь можно генерировать посты в стиле авторов!

