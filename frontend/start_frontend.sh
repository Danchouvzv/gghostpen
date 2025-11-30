#!/bin/bash
# Скрипт запуска GhostPen Frontend

cd "$(dirname "$0")"

echo "🚀 Запуск GhostPen Frontend..."
echo "📁 Рабочая директория: $(pwd)"

# Проверка node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 Установка зависимостей..."
    npm install
fi

# Запуск dev сервера
echo "✅ Запуск Frontend на http://localhost:5173"
echo ""
npm run dev

