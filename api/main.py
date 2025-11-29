#!/usr/bin/env python3
"""
FastAPI Backend для GhostPen.

Предоставляет REST API для генерации постов в авторском стиле.
"""

import time
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Добавляем путь к скриптам
scripts_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from ghostpen_generator import GhostPenGenerator
from style_scorer import StyleScorer
import json
import os

app = FastAPI(
    title="GhostPen API",
    description="API для генерации постов в авторском стиле",
    version="1.0.0"
)

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Загружаем профили при старте
PROFILES_PATH = Path(__file__).parent.parent / "dataset" / "author_profiles.json"
generator: Optional[GhostPenGenerator] = None
scorer: Optional[StyleScorer] = None

@app.on_event("startup")
async def startup_event():
    """Инициализация при старте сервера."""
    global generator, scorer
    
    if not PROFILES_PATH.exists():
        raise FileNotFoundError(f"Профили не найдены: {PROFILES_PATH}")
    
    # Инициализируем генератор
    # Для реальной работы передайте OPENAI_API_KEY через переменную окружения
    api_key = os.getenv("OPENAI_API_KEY")  # None = mock режим
    generator = GhostPenGenerator(PROFILES_PATH, api_key)
    scorer = StyleScorer()
    
    print(f"✅ GhostPen API запущен. Профили загружены из {PROFILES_PATH}")


# Pydantic модели для запросов/ответов
class GenerateRequest(BaseModel):
    author_id: str = Field(..., description="ID автора")
    social_network: str = Field(..., description="Социальная сеть: linkedin, instagram, facebook, telegram")
    topic: str = Field(..., description="Тема поста")
    sample_posts: Optional[list[str]] = Field(default=[], description="Примеры постов (опционально)")


class DebugInfo(BaseModel):
    target_length: int
    model_version: str
    processing_time_ms: int
    prompt_tokens: int


class GenerateResponse(BaseModel):
    generated_post: str
    style_similarity: float
    debug: DebugInfo


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {
        "service": "GhostPen API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "generate": "/api/generate",
            "authors": "/api/authors",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health():
    """Проверка здоровья сервиса."""
    return {
        "status": "healthy",
        "profiles_loaded": generator is not None,
        "profiles_path": str(PROFILES_PATH)
    }


@app.get("/api/authors")
async def get_authors():
    """Получить список доступных авторов."""
    if not PROFILES_PATH.exists():
        raise HTTPException(status_code=500, detail="Профили не найдены")
    
    # Маппинг имен и профессий для авторов
    author_info = {
        "person_01": {"name": "Дмитрий Петров", "profession": "Team Lead"},
        "person_02": {"name": "Айдар Нурланов", "profession": "Tech Lead"},
        "person_03": {"name": "Ерлан Токтаров", "profession": "Backend Developer"},
        "person_04": {"name": "Алия Сейтжанова", "profession": "UX Designer"},
        "person_05": {"name": "Данияр Касымов", "profession": "Startup Founder"},
        "person_06": {"name": "Жанар Абдуллина", "profession": "Life Coach"},
        "person_07": {"name": "Мария Соколова", "profession": "Marketing Director"},
        "person_08": {"name": "Айгуль Мусаева", "profession": "Rust Engineer"},
        "person_09": {"name": "Асхат Беков", "profession": "Visual Designer"},
        "person_10": {"name": "Алексей Волков", "profession": "Business Consultant"}
    }
    
    with open(PROFILES_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    authors = []
    for profile in data.get('profiles', []):
        style = profile.get('style', {})
        tone = style.get('tone', {})
        author_id = profile['author_id']
        
        # Получаем имя и профессию из маппинга
        info = author_info.get(author_id, {
            "name": author_id.replace('_', ' ').title(),
            "profession": "Content Creator"
        })
        
        authors.append({
            "id": author_id,
            "name": info["name"],
            "profession": info["profession"],
            "total_posts": profile.get('total_posts', 0),
            "platforms": profile.get('platforms', []),
            "sample_posts": profile.get('sample_posts', []),
            "stats": {
                "formality": tone.get('dominant', 'balanced'),
                "avgLength": style.get('avg_post_length', 300),
                "emojiDensity": "High" if style.get('emoji_density', 0) > 1 else "Low"
            }
        })
    
    return {"authors": authors}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_post(request: GenerateRequest):
    """
    Генерирует пост в стиле автора.
    
    Args:
        request: Запрос с параметрами генерации
        
    Returns:
        Сгенерированный пост с метриками
    """
    if generator is None or scorer is None:
        raise HTTPException(status_code=500, detail="Генератор не инициализирован")
    
    # Валидация платформы
    valid_platforms = ['linkedin', 'instagram', 'facebook', 'telegram']
    if request.social_network not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемая платформа. Доступны: {', '.join(valid_platforms)}"
        )
    
    start_time = time.time()
    
    try:
        # Генерируем пост
        result = generator.generate_post(
            author_id=request.author_id,
            platform=request.social_network,
            topic=request.topic,
            additional_context=None  # Можно использовать sample_posts в будущем
        )
        
        # Получаем профиль для оценки
        profile = generator.prompt_builder.profiles.get(request.author_id)
        if not profile:
            raise HTTPException(status_code=404, detail=f"Автор {request.author_id} не найден")
        
        # Оцениваем стилевое сходство
        similarity_scores = scorer.score(
            result['generated_post'],
            profile,
            request.social_network
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Подсчитываем примерное количество токенов в промпте
        prompt_tokens = len(result.get('prompt_used', '').split()) * 1.3  # Примерная оценка
        
        # Формируем ответ в формате, ожидаемом фронтендом
        response = GenerateResponse(
            generated_post=result['generated_post'],
            style_similarity=round(similarity_scores['overall_score'], 2),
            debug=DebugInfo(
                target_length=result['metrics']['target_length'],
                model_version="ghostpen-v1.0",
                processing_time_ms=processing_time,
                prompt_tokens=int(prompt_tokens)
            )
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

