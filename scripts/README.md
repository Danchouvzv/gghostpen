# 🔧 GhostPen Scripts

Скрипты для работы с GhostPen.

## 📋 Доступные скрипты

### 1. `prepare_dataset.py` — Валидация и статистика датасета

```bash
# Валидация датасета
python scripts/prepare_dataset.py validate dataset/dataset.json dataset/schema.json

# Статистика датасета
python scripts/prepare_dataset.py stats dataset/dataset.json
```

### 2. `style_profiler.py` — Генерация стилевых профилей

Анализирует посты авторов и создаёт стилевые профили.

```bash
python scripts/style_profiler.py dataset/dataset.json dataset/author_profiles.json
```

**Что делает:**
- Анализирует стиль каждого автора
- Извлекает метрики (длина, тон, структура, эмодзи, хэштеги)
- Определяет тематику и характерные фразы
- Создаёт платформо-специфичные профили

### 3. `prompt_builder.py` — Построение промптов

Строит промпты для LLM на основе профилей авторов.

```bash
python scripts/prompt_builder.py dataset/author_profiles.json person_01 linkedin "О важности планирования"
```

**Что делает:**
- Загружает профили авторов
- Строит детальный промпт с:
  - Стилевыми характеристиками
  - Примерами постов
  - Правилами платформы
  - Требованиями к формату

### 4. `ghostpen_generator.py` — Генерация постов

Полный pipeline генерации постов.

```bash
# С mock LLM (для тестирования)
python scripts/ghostpen_generator.py dataset/author_profiles.json person_01 linkedin "О важности планирования"

# С OpenAI API
python scripts/ghostpen_generator.py dataset/author_profiles.json person_01 linkedin "О важности планирования" YOUR_API_KEY
```

**Что делает:**
1. Строит промпт через Prompt Builder
2. Генерирует текст через LLM
3. Применяет post-processing:
   - Корректирует длину
   - Убирает повторы
   - Настраивает эмодзи и структуру

### 5. `style_scorer.py` — Оценка стилевого сходства

Оценивает, насколько сгенерированный пост соответствует стилю автора.

```bash
# Сохраните сгенерированный пост в файл
echo "Ваш пост..." > generated_post.txt

# Оцените
python scripts/style_scorer.py dataset/author_profiles.json person_01 linkedin generated_post.txt
```

**Метрики:**
- `length_accuracy` — соответствие длины
- `sentence_length_match` — соответствие длины предложений
- `emoji_density_match` — соответствие плотности эмодзи
- `hashtag_density_match` — соответствие плотности хэштегов
- `structure_match` — соответствие структуры
- `tone_match` — соответствие тона
- `emotionality_match` — соответствие эмоциональности
- `overall_score` — общая оценка (0-1)

## 🔄 Полный pipeline

```bash
# 1. Подготовка датасета
python scripts/prepare_dataset.py validate dataset/dataset.json dataset/schema.json

# 2. Генерация профилей
python scripts/style_profiler.py dataset/dataset.json dataset/author_profiles.json

# 3. Генерация поста
python scripts/ghostpen_generator.py dataset/author_profiles.json person_01 linkedin "Тема поста" > generated_post.txt

# 4. Оценка качества
python scripts/style_scorer.py dataset/author_profiles.json person_01 linkedin generated_post.txt
```

## 📦 Зависимости

```bash
pip install -r scripts/requirements.txt
```

Для использования OpenAI API:
```bash
pip install openai
```

## 🎯 Примеры использования

### Генерация поста для LinkedIn

```bash
python scripts/ghostpen_generator.py \
  dataset/author_profiles.json \
  person_01 \
  linkedin \
  "О важности обратной связи в команде"
```

### Генерация поста для Instagram

```bash
python scripts/ghostpen_generator.py \
  dataset/author_profiles.json \
  person_02 \
  instagram \
  "Мотивация на понедельник"
```

### Оценка качества

```bash
python scripts/style_scorer.py \
  dataset/author_profiles.json \
  person_01 \
  linkedin \
  generated_post.txt
```

## 🔍 Структура

```
scripts/
├── prepare_dataset.py      # Валидация датасета
├── style_profiler.py       # Анализ стиля
├── prompt_builder.py       # Построение промптов
├── ghostpen_generator.py   # Генерация постов
├── style_scorer.py         # Оценка качества
├── requirements.txt        # Зависимости
└── README.md              # Эта документация
```

