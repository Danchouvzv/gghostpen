#!/usr/bin/env python3
"""
FastAPI Backend для GhostPen.

Предоставляет REST API для генерации постов в авторском стиле.
"""

import time
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Rate Limiting (опционально)
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    RATE_LIMIT_AVAILABLE = True
except ImportError:
    RATE_LIMIT_AVAILABLE = False
    print("⚠️ [RATE_LIMIT] slowapi не установлен, rate limiting отключен")

# Загружаем переменные окружения из .env файла
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ [ENV] .env файл загружен")
except ImportError:
    print("⚠️ [ENV] python-dotenv не установлен, используем системные переменные окружения")

# Добавляем путь к скриптам
scripts_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from ghostpen_generator import GhostPenGenerator
from style_scorer import StyleScorer
from database import Database
from style_profiler import StyleProfiler
import json
import os
import uuid

app = FastAPI(
    title="GhostPen API",
    description="API для генерации постов в авторском стиле",
    version="1.1.0"
)

# Rate Limiting (опционально)
if RATE_LIMIT_AVAILABLE:
    try:
        limiter = Limiter(key_func=get_remote_address)
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        RATE_LIMIT_ENABLED = True
        print("✅ [RATE_LIMIT] Rate limiting активирован (10 запросов/минуту)")
    except Exception as e:
        print(f"⚠️ [RATE_LIMIT] Rate limiting не активирован: {e}")
        RATE_LIMIT_ENABLED = False
else:
    RATE_LIMIT_ENABLED = False

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
db: Optional[Database] = None
profiler: Optional[StyleProfiler] = None

@app.on_event("startup")
async def startup_event():
    """Инициализация при старте сервера."""
    global generator, scorer, db, profiler
    
    # Инициализируем БД
    db = Database()
    
    # Инициализируем StyleProfiler
    profiler = StyleProfiler()
    
    if not PROFILES_PATH.exists():
        print(f"ℹ️  Демо-профили не найдены: {PROFILES_PATH}")
        print(f"   Система будет работать только с персональными профилями пользователей из БД")
    else:
        # Инициализируем генератор для демо-авторов (опционально)
        # Для реальной работы передайте OPENAI_API_KEY через переменную окружения
        api_key = os.getenv("OPENAI_API_KEY")  # None = mock режим
        generator = GhostPenGenerator(PROFILES_PATH, api_key)
        scorer = StyleScorer()
        print(f"✅ GhostPen API запущен. Демо-профили загружены из {PROFILES_PATH}")


# Pydantic модели для запросов/ответов
class GenerateRequest(BaseModel):
    author_id: Optional[str] = Field(None, description="ID автора (для демо) или user_id")
    user_id: Optional[str] = Field(None, description="ID пользователя (для персональных профилей)")
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
async def get_authors(user_id: Optional[str] = None):
    """Получить список доступных авторов."""
    print(f"📥 [API] Запрос авторов, user_id: {user_id}")
    authors = []
    
    # Добавляем демо-авторов (опционально, только если файл существует)
    if PROFILES_PATH.exists():
        # Маппинг имен и профессий для авторов
        author_info = {
            "person_01": {"name": "Айдар Нұрғалиев", "profession": "CEO & Основатель"},
            "person_02": {"name": "Асылбек Қасымов", "profession": "Маркетолог"},
            "person_03": {"name": "Ерлан Сағындықов", "profession": "Backend Разработчик"},
            "person_04": {"name": "Жанар Әбілқасымова", "profession": "UI/UX Дизайнер"},
            "person_05": {"name": "Нұрлан Байжанов", "profession": "Предприниматель"},
            "person_06": {"name": "Алма Төлеуова", "profession": "Психолог"},
            "person_07": {"name": "Данияр Мұхамеджанов", "profession": "Digital Маркетолог"},
            "person_08": {"name": "Руслан Петров", "profession": "Rust Инженер"},
            "person_09": {"name": "Анна Смирнова", "profession": "Визуальный Дизайнер"},
            "person_10": {"name": "Дмитрий Иванов", "profession": "Бизнес-Консультант"},
        }
        
        with open(PROFILES_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
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
                "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={author_id}",
                "platforms": profile.get('platforms', []),
                "sample_posts": profile.get('sample_posts', []),
                "stats": {
                    "total_posts": profile.get('total_posts', 0),
                    "platforms_count": len(profile.get('platforms', [])),
                    "formality": tone.get('dominant', 'balanced'),
                    "avgLength": style.get('avg_post_length', 300),
                    "emojiDensity": "High" if style.get('emoji_density', 0) > 1 else "Low"
                },
                "is_demo": True
            })
    
    # Добавляем профиль текущего пользователя, если он залогинен
    if user_id:
        print(f"🔍 [API] Поиск пользователя: {user_id}")
        user = db.get_user(user_id)
        print(f"🔍 [API] Результат get_user: {user}")
        if user:  # Пользователь существует
            print(f"✅ [API] Пользователь найден: {user.get('name', 'N/A')}")
            user_posts = db.get_user_posts(user_id)
            user_profile = db.get_profile(user_id)
            print(f"📊 [API] Постов: {len(user_posts)}, Профиль: {'есть' if user_profile else 'нет'}")
            
            # Если есть профиль, используем его данные, иначе дефолтные
            if user_profile:
                platforms = list(set([p["platform"] for p in user_posts])) if user_posts else []
                authors.insert(0, {
                    "id": f"user_{user_id}",
                    "name": user.get("name", "Мой профиль"),
                    "profession": "Ваш стиль",
                    "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_id}",
                    "platforms": platforms,
                    "sample_posts": user_profile.get("sample_posts", []),
                    "stats": {
                        "total_posts": len(user_posts),
                        "platforms_count": len(platforms),
                        "formality": user_profile.get("style", {}).get("tone", {}).get("dominant", "balanced"),
                        "avgLength": user_profile.get("style", {}).get("avg_post_length", 300),
                        "emojiDensity": "High" if user_profile.get("style", {}).get("emoji_density", 0) > 1 else "Low"
                    },
                    "is_demo": False,
                    "user_id": user_id
                })
            else:
                # Пользователь есть, но профиль не перестроен - показываем с предупреждением
                platforms = list(set([p["platform"] for p in user_posts])) if user_posts else []
                authors.insert(0, {
                    "id": f"user_{user_id}",
                    "name": user.get("name", "Мой профиль"),
                    "profession": "Перестройте профиль" if user_posts else "Добавьте посты",
                    "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_id}",
                    "platforms": platforms,
                    "sample_posts": [],
                    "stats": {
                        "total_posts": len(user_posts),
                        "platforms_count": len(platforms),
                        "formality": "balanced",
                        "avgLength": 300,
                        "emojiDensity": "Low"
                    },
                    "is_demo": False,
                    "user_id": user_id,
                    "needs_rebuild": True  # Флаг, что нужно перестроить профиль
                })
        else:
            print(f"⚠️ [API] Пользователь не найден в БД: {user_id}")
            # Попробуем создать пользователя, если его нет (на случай если он был создан, но не сохранился)
            print(f"🔧 [API] Попытка создать пользователя...")
            db.create_user(user_id, name="Пользователь")
            user = db.get_user(user_id)
            if user:
                print(f"✅ [API] Пользователь создан, добавляем в список")
                authors.insert(0, {
                    "id": f"user_{user_id}",
                    "name": user.get("name", "Мой профиль"),
                    "profession": "Добавьте посты",
                    "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_id}",
                    "platforms": [],
                    "sample_posts": [],
                    "stats": {
                        "total_posts": 0,
                        "platforms_count": 0,
                        "formality": "balanced",
                        "avgLength": 300,
                        "emojiDensity": "Low"
                    },
                    "is_demo": False,
                    "user_id": user_id,
                    "needs_rebuild": True
                })
    
    print(f"📤 [API] Возвращаем {len(authors)} авторов")
    return {"authors": authors}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_post(request_data: GenerateRequest):
    """
    Генерирует пост в стиле автора.
    
    Args:
        request: FastAPI Request объект
        request_data: Запрос с параметрами генерации
        
    Returns:
        Сгенерированный пост с метриками
    """
    # Улучшенная валидация входных данных
    if not request_data.topic or len(request_data.topic.strip()) < 3:
        raise HTTPException(status_code=400, detail="Тема поста слишком короткая (минимум 3 символа)")
    
    if len(request_data.topic) > 500:
        raise HTTPException(status_code=400, detail="Тема поста слишком длинная (максимум 500 символов)")
    
    # Валидация платформы
    valid_platforms = ['linkedin', 'instagram', 'facebook', 'telegram']
    if request_data.social_network not in valid_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемая платформа. Доступны: {', '.join(valid_platforms)}"
        )
    
    # Проверка инициализации (только для демо-авторов)
    if request_data.author_id and (generator is None or scorer is None):
        raise HTTPException(
            status_code=500, 
            detail="Генератор не инициализирован. Проверьте наличие dataset/author_profiles.json"
        )
    
    start_time = time.time()
    
    try:
        # Определяем, используем ли мы user_id или author_id
        if request_data.user_id:
            # Работа с персональным профилем пользователя
            user_profile = db.get_profile(request_data.user_id)
            if not user_profile:
                raise HTTPException(status_code=404, detail="Профиль пользователя не найден. Используйте /rebuild-profile")
            
            # Оптимизированная работа с временными файлами
            import tempfile
            import atexit
            
            # Создаём временный файл с профилем пользователя
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
            temp_path = Path(temp_file.name)
            
            try:
                temp_profile = {
                    "version": "1.0",
                    "profiles": [user_profile]
                }
                json.dump(temp_profile, temp_file, ensure_ascii=False)
                temp_file.close()
                
                # Регистрируем удаление файла при выходе
                atexit.register(lambda: temp_path.unlink() if temp_path.exists() else None)
                
                api_key = os.getenv("OPENAI_API_KEY")
                print(f"🔑 [GENERATE] Проверка API ключа:")
                print(f"   - OPENAI_API_KEY в окружении: {'есть' if api_key else 'НЕТ'}")
                if api_key:
                    print(f"   - Длина ключа: {len(api_key)} символов")
                    print(f"   - Первые 10 символов: {api_key[:10]}...")
                    print(f"   - Начинается с 'sk-': {api_key.startswith('sk-')}")
                else:
                    print(f"   ⚠️ API ключ НЕ установлен - будет использоваться MOCK генерация")
                
                user_generator = GhostPenGenerator(temp_path, api_key)
                user_scorer = StyleScorer()
            except Exception as e:
                # Удаляем временный файл в случае ошибки
                if temp_path.exists():
                    temp_path.unlink()
                raise
            
            # Логируем информацию о профиле пользователя
            sample_posts_count = len(user_profile.get('sample_posts', []))
            style = user_profile.get('style', {})
            tone = style.get('tone', {})
            
            print(f"📝 [GENERATE] Профиль пользователя:")
            print(f"   - author_id: {user_profile['author_id']}")
            print(f"   - sample_posts в профиле: {sample_posts_count}")
            if sample_posts_count > 0:
                print(f"   - Первый пост (первые 100 символов): {user_profile['sample_posts'][0][:100]}...")
            
            print(f"📊 [GENERATE] Извлечённые метрики стиля:")
            print(f"   - Средняя длина поста: {style.get('avg_post_length', 'N/A')} символов")
            print(f"   - Средняя длина предложения: {style.get('avg_sentence_length', 'N/A'):.2f} слов" if style.get('avg_sentence_length') else "   - Средняя длина предложения: N/A")
            print(f"   - Плотность эмодзи: {style.get('emoji_density', 0):.2f}")
            print(f"   - Плотность хэштегов: {style.get('hashtag_density', 0):.2f}")
            print(f"   - Эмоциональность: {style.get('emotionality', 0):.2f}")
            print(f"   - Тип структуры: {style.get('structure_type', 'N/A')}")
            print(f"   - Доминирующий тон: {tone.get('dominant', 'N/A')}")
            print(f"   - Характерных фраз: {len(user_profile.get('signature_phrases', []))}")
            
            try:
                result = user_generator.generate_post(
                    author_id=user_profile['author_id'],
                    platform=request_data.social_network,
                    topic=request_data.topic,
                    additional_context=None
                )
                
                # Логируем промпт, который был использован
                if 'prompt_used' in result:
                    prompt = result['prompt_used']
                    if 'ПРИМЕРЫ ПОСТОВ' in prompt:
                        print(f"✅ [GENERATE] Промпт содержит раздел 'ПРИМЕРЫ ПОСТОВ' - ваши посты используются!")
                        # Извлекаем секцию с примерами
                        examples_start = prompt.find('ПРИМЕРЫ ПОСТОВ')
                        if examples_start != -1:
                            examples_end = prompt.find('\n\nТРЕБОВАНИЯ ПЛАТФОРМЫ:', examples_start)
                            if examples_end == -1:
                                examples_end = prompt.find('\n\nТЕМА ПОСТА:', examples_start)
                            if examples_end != -1:
                                examples_section = prompt[examples_start:examples_end]
                                print(f"📄 [GENERATE] Секция с примерами (первые 300 символов):")
                                print(f"   {examples_section[:300]}...")
                    else:
                        print(f"⚠️ [GENERATE] Промпт НЕ содержит 'ПРИМЕРЫ ПОСТОВ' - проверьте sample_posts")
                        print(f"📄 [GENERATE] Промпт (первые 500 символов):")
                        print(f"   {prompt[:500]}...")
                
                similarity_scores = user_scorer.score(
                    result['generated_post'],
                    user_profile,
                    request_data.social_network
                )
            finally:
                # Удаляем временный файл после использования
                if temp_path.exists():
                    try:
                        temp_path.unlink()
                        print(f"🗑️ [GENERATE] Временный файл удалён: {temp_path}")
                    except Exception as e:
                        print(f"⚠️ [GENERATE] Не удалось удалить временный файл: {e}")
            
        else:
            # Работа с демо-авторами
            if not request_data.author_id:
                raise HTTPException(status_code=400, detail="Укажите author_id или user_id")
            
            if generator is None:
                raise HTTPException(status_code=500, detail="Генератор не инициализирован")
            
            result = generator.generate_post(
                author_id=request_data.author_id,
                platform=request_data.social_network,
                topic=request_data.topic,
                additional_context=None
            )
            
            # Получаем профиль для оценки
            profile = generator.prompt_builder.profiles.get(request_data.author_id)
            if not profile:
                raise HTTPException(status_code=404, detail=f"Автор {request_data.author_id} не найден")
            
            # Оцениваем стилевое сходство
            similarity_scores = scorer.score(
                result['generated_post'],
                profile,
                request_data.social_network
            )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Улучшенный подсчет токенов (более точная оценка)
        prompt_text = result.get('prompt_used', '')
        # Примерная оценка: 1 токен ≈ 0.75 слова для русского языка
        prompt_tokens = int(len(prompt_text.split()) * 0.75)
        
        # Формируем ответ в формате, ожидаемом фронтендом
        response = GenerateResponse(
            generated_post=result['generated_post'],
            style_similarity=round(similarity_scores.get('overall_score', 0.7), 2),
            debug=DebugInfo(
                target_length=result.get('metrics', {}).get('target_length', 300),
                model_version="ghostpen-v1.1-enhanced",
                processing_time_ms=processing_time,
                prompt_tokens=prompt_tokens
            )
        )
        
        return response
        
    except HTTPException:
        raise
    except ValueError as e:
        # Валидационные ошибки
        raise HTTPException(status_code=400, detail=f"Ошибка валидации: {str(e)}")
    except FileNotFoundError as e:
        # Ошибки файлов
        raise HTTPException(status_code=404, detail=f"Файл не найден: {str(e)}")
    except Exception as e:
        # Общие ошибки с улучшенным логированием
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ [GENERATE] Критическая ошибка: {str(e)}")
        print(f"📋 [GENERATE] Traceback:\n{error_trace}")
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка генерации: {str(e)}"
        )


# === User Management ===

class CreateUserRequest(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None


class AddPostRequest(BaseModel):
    platform: str = Field(..., description="Платформа: linkedin, instagram, facebook, telegram")
    content: str = Field(..., description="Текст поста")
    timestamp: Optional[str] = None
    hashtags: Optional[list[str]] = Field(default=[])
    mentions: Optional[list[str]] = Field(default=[])
    emojis: Optional[list[str]] = Field(default=[])


@app.post("/api/users")
async def create_user(request: CreateUserRequest):
    """Создать нового пользователя."""
    user_id = str(uuid.uuid4())
    if db.create_user(user_id, request.email, request.name):
        return {"user_id": user_id, "status": "created"}
    raise HTTPException(status_code=400, detail="Пользователь уже существует")


@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Получить информацию о пользователе."""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.post("/api/users/{user_id}/posts")
async def add_post(user_id: str, request: AddPostRequest):
    """Добавить пост пользователя."""
    # Проверяем существование пользователя
    if not db.get_user(user_id):
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    valid_platforms = ['linkedin', 'instagram', 'facebook', 'telegram']
    if request.platform not in valid_platforms:
        raise HTTPException(status_code=400, detail=f"Неподдерживаемая платформа")
    
    post_id = db.add_post(
        user_id=user_id,
        platform=request.platform,
        content=request.content,
        timestamp=request.timestamp,
        hashtags=request.hashtags,
        mentions=request.mentions,
        emojis=request.emojis
    )
    return {"post_id": post_id, "status": "created"}


@app.get("/api/users/{user_id}/posts")
async def get_user_posts(user_id: str, platform: Optional[str] = None):
    """Получить посты пользователя."""
    posts = db.get_user_posts(user_id, platform)
    return {"posts": posts, "count": len(posts)}


@app.delete("/api/users/{user_id}/posts/{post_id}")
async def delete_post(user_id: str, post_id: str):
    """Удалить пост пользователя."""
    if db.delete_post(post_id, user_id):
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Пост не найден")


@app.post("/api/users/{user_id}/rebuild-profile")
async def rebuild_profile(user_id: str):
    """Перестроить стилевой профиль пользователя."""
    # Получаем данные пользователя
    user_data = db.get_user_data_for_profiling(user_id)
    if not user_data:
        raise HTTPException(status_code=400, detail="У пользователя нет постов")
    
    # Анализируем стиль
    profile = profiler.analyze_author(user_data)
    
    # Сохраняем профиль
    db.save_profile(user_id, profile)
    
    return {
        "status": "success",
        "profile": profile,
        "total_posts": sum(len(posts) for posts in user_data['platforms'].values())
    }


@app.get("/api/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Получить стилевой профиль пользователя."""
    profile = db.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден. Используйте /rebuild-profile")
    return profile


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

