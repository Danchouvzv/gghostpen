#!/bin/bash
# Скрипт запуска GhostPen Backend

cd "$(dirname "$0")"

echo "🚀 Запуск GhostPen Backend..."
echo "📁 Рабочая директория: $(pwd)"

# Проверка зависимостей
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Установка зависимостей..."
    pip3 install -q -r api/requirements.txt
fi

# Проверка профилей
if [ ! -f "dataset/author_profiles.json" ]; then
    echo "⚠️  Профили не найдены. Генерирую..."
    python3 scripts/style_profiler.py dataset/dataset.json dataset/author_profiles.json
fi

# Загрузка .env файла если есть
if [ -f "api/.env" ]; then
    export $(cat api/.env | grep -v '^#' | xargs)
    echo "✅ .env файл загружен из api/.env"
fi

# Проверка OpenAI API ключа
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY не установлен. Используется mock генерация."
    echo "💡 Для реальной генерации создайте api/.env с OPENAI_API_KEY='sk-...'"
else
    echo "✅ OpenAI API ключ найден. Используется реальная генерация."
fi

# Запуск сервера
echo "✅ Запуск API на http://localhost:8000"
echo "📖 Документация: http://localhost:8000/docs"
echo ""
cd api
python3 main.py

