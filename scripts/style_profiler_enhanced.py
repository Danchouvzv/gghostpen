#!/usr/bin/env python3
"""
Улучшенный Style Profiler для GhostPen.

Добавлены:
- Более умный анализ тона (контекстный)
- Улучшенное извлечение signature phrases
- Кэширование результатов
- Валидация данных
"""

import json
import re
import statistics
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache


class EnhancedStyleProfiler:
    """Улучшенный анализатор стиля автора."""
    
    # Расширенные словари для определения тона
    FORMAL_WORDS = ['понимаю', 'применяю', 'рекомендую', 'следует', 'необходимо', 
                    'важно', 'ключевой', 'принцип', 'подход', 'методология', 'реализация',
                    'внедрение', 'оптимизация', 'стратегия', 'тактика', 'процесс']
    EMOTIONAL_WORDS = ['чувствую', 'люблю', 'нравится', 'волнуюсь', 'страшно', 
                       'интересно', 'удивительно', 'вдохновляет', 'радует', 'восторг',
                       'восхищаюсь', 'переживаю', 'волнуюсь', 'тревожусь']
    EXPERT_WORDS = ['анализ', 'решение', 'оптимизация', 'архитектура', 'метрики',
                    'стратегия', 'трансформация', 'процесс', 'система', 'фреймворк',
                    'методология', 'инструмент', 'технология', 'алгоритм']
    CASUAL_WORDS = ['кстати', 'вообще', 'короче', 'типа', 'как бы', 'в общем', 'ну',
                    'вот', 'так', 'это', 'же', 'да', 'нет']
    
    # Расширенный список стоп-фраз
    STOP_PHRASES = {
        'вчера на', 'сегодня я', 'сегодня утром', 'сегодня вечером', 'на этой неделе',
        'за последние', 'недавно я', 'недавно мы', 'вчера получил', 'сегодня начал',
        'это не', 'это про', 'что вы', 'как вы', 'это значит', 'это то', 'это как',
        'когда мы', 'когда ты', 'когда я', 'если вы', 'если мы', 'если ты',
        'для того', 'для вас', 'для нас', 'для меня', 'для тебя',
        'может быть', 'всегда есть', 'всегда можно', 'всегда нужно', 'всегда важно',
        'очень важно', 'очень интересно', 'очень полезно',
        'не только', 'не просто', 'не всегда', 'не обязательно',
        'то есть', 'так что', 'и это', 'но это', 'или это',
        'что думаете', 'что вы думаете', 'как вы думаете',
        'а также', 'и ещё', 'но и'
    }
    
    TOPICS = {
        'career': ['карьера', 'работа', 'профессия', 'команда', 'проект', 'лидерство', 'менеджмент'],
        'motivation': ['мотивация', 'цель', 'рост', 'развитие', 'успех', 'достижение', 'вдохновение'],
        'personal': ['личный', 'опыт', 'история', 'размышление', 'мысль', 'чувство'],
        'expertise': ['технология', 'инструмент', 'метод', 'подход', 'решение', 'оптимизация'],
        'business': ['бизнес', 'стартап', 'клиент', 'продукт', 'рынок', 'стратегия']
    }
    
    def __init__(self):
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        self._cache = {}
    
    def analyze_author(self, author_data: Dict[str, Any], use_cache: bool = True) -> Dict[str, Any]:
        """
        Анализирует стиль автора с улучшенными алгоритмами.
        
        Args:
            author_data: Данные автора
            use_cache: Использовать кэш
            
        Returns:
            Стилевой профиль автора
        """
        author_id = author_data.get("author_id", "unknown")
        
        # Проверка кэша
        if use_cache and author_id in self._cache:
            return self._cache[author_id]
        
        # Валидация входных данных
        if not self._validate_author_data(author_data):
            raise ValueError(f"Невалидные данные автора: {author_id}")
        
        all_posts = []
        for platform, posts in author_data.get("platforms", {}).items():
            for post in posts:
                if isinstance(post, dict) and "content" in post:
                    all_posts.append({
                        "content": post["content"],
                        "platform": platform,
                        "meta": post.get("meta", {})
                    })
        
        if not all_posts:
            raise ValueError(f"Нет постов для анализа: {author_id}")
        
        # Улучшенный анализ
        profile = {
            "author_id": author_id,
            "total_posts": len(all_posts),
            "platforms": list(author_data.get("platforms", {}).keys()),
            "style": self._analyze_style_enhanced(all_posts),
            "sample_posts": self._get_sample_posts(all_posts, max_samples=5),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Кэширование
        if use_cache:
            self._cache[author_id] = profile
        
        return profile
    
    def _validate_author_data(self, data: Dict[str, Any]) -> bool:
        """Валидация данных автора."""
        if not isinstance(data, dict):
            return False
        if "author_id" not in data:
            return False
        if "platforms" not in data or not isinstance(data["platforms"], dict):
            return False
        return True
    
    def _analyze_style_enhanced(self, posts: List[Dict]) -> Dict[str, Any]:
        """Улучшенный анализ стиля с контекстным анализом тона."""
        all_text = " ".join([p["content"] for p in posts])
        words = all_text.split()
        
        return {
            "avg_post_length": int(statistics.mean([len(p["content"]) for p in posts])),
            "min_post_length": min([len(p["content"]) for p in posts]),
            "max_post_length": max([len(p["content"]) for p in posts]),
            "avg_sentence_length": self._calculate_avg_sentence_length(posts),
            "avg_paragraphs": statistics.mean([p["content"].count('\n\n') + 1 for p in posts]),
            "uses_lists": self._detect_list_usage(posts),
            "emoji_density": self._calculate_emoji_density(posts),
            "hashtag_density": self._calculate_hashtag_density(posts),
            "tone": self._analyze_tone_enhanced(all_text, posts),
            "emotionality": self._calculate_emotionality_enhanced(all_text, posts),
            "structure_type": self._detect_structure_type(posts),
            "topics": self._detect_topics(posts),
            "signature_phrases": self._extract_phrases_enhanced(posts, max_phrases=7)
        }
    
    def _calculate_avg_sentence_length(self, posts: List[Dict]) -> float:
        """Вычисляет среднюю длину предложений в словах."""
        all_sentences = []
        for post in posts:
            sentences = re.split(r'[.!?]+', post["content"])
            for sent in sentences:
                words = [w for w in sent.split() if w]
                if words:
                    all_sentences.append(len(words))
        return statistics.mean(all_sentences) if all_sentences else 0.0
    
    def _detect_list_usage(self, posts: List[Dict]) -> bool:
        """Определяет, использует ли автор списки."""
        list_patterns = [
            r'^\d+\.',  # Нумерованные
            r'^[-•*]',  # Маркированные
            r'^\s*[-•*]\s'  # С отступом
        ]
        for post in posts:
            for pattern in list_patterns:
                if re.search(pattern, post["content"], re.MULTILINE):
                    return True
        return False
    
    def _calculate_emoji_density(self, posts: List[Dict]) -> float:
        """Вычисляет плотность эмодзи."""
        total_emojis = sum(len(self.emoji_pattern.findall(p["content"])) for p in posts)
        total_chars = sum(len(p["content"]) for p in posts)
        return round(total_emojis / max(total_chars, 1) * 1000, 2)
    
    def _calculate_hashtag_density(self, posts: List[Dict]) -> float:
        """Вычисляет плотность хэштегов."""
        total_hashtags = sum(len(re.findall(r'#\w+', p["content"])) for p in posts)
        total_chars = sum(len(p["content"]) for p in posts)
        return round(total_hashtags / max(total_chars, 1) * 1000, 2)
    
    def _analyze_tone_enhanced(self, text: str, posts: List[Dict]) -> Dict[str, float]:
        """Улучшенный анализ тона с контекстным учетом."""
        text_lower = text.lower()
        words = text_lower.split()
        
        # Базовые подсчеты
        formal_count = sum(1 for word in words if word in self.FORMAL_WORDS)
        emotional_count = sum(1 for word in words if word in self.EMOTIONAL_WORDS)
        expert_count = sum(1 for word in words if word in self.EXPERT_WORDS)
        casual_count = sum(1 for word in words if word in self.CASUAL_WORDS)
        
        # Контекстные признаки
        has_questions = sum(1 for p in posts if '?' in p["content"]) > len(posts) * 0.3
        has_exclamations = sum(1 for p in posts if '!' in p["content"]) > len(posts) * 0.3
        avg_length = statistics.mean([len(p["content"]) for p in posts])
        
        # Взвешенные оценки
        formal_score = (formal_count / max(len(words), 1) * 1000) + (1 if avg_length > 400 else 0)
        emotional_score = (emotional_count / max(len(words), 1) * 1000) + (2 if has_exclamations else 0)
        expert_score = (expert_count / max(len(words), 1) * 1000) + (1 if avg_length > 500 else 0)
        casual_score = (casual_count / max(len(words), 1) * 1000) + (1 if has_questions else 0)
        
        scores = {
            "formal": round(formal_score, 2),
            "emotional": round(emotional_score, 2),
            "expert": round(expert_score, 2),
            "casual": round(casual_score, 2)
        }
        
        dominant = max(scores.items(), key=lambda x: x[1])[0]
        scores["dominant"] = dominant
        
        return scores
    
    def _calculate_emotionality_enhanced(self, text: str, posts: List[Dict]) -> float:
        """Улучшенный расчет эмоциональности."""
        emotional_words = sum(1 for word in self.EMOTIONAL_WORDS if word in text.lower())
        emojis_count = sum(len(self.emoji_pattern.findall(p["content"])) for p in posts)
        exclamation_count = sum(p["content"].count('!') for p in posts)
        question_count = sum(p["content"].count('?') for p in posts)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        # Улучшенная формула
        emotionality = (
            emotional_words * 2 + 
            emojis_count * 3 + 
            exclamation_count * 1.5 + 
            question_count * 0.5
        ) / total_words * 100
        
        return min(round(emotionality, 2), 10.0)
    
    def _detect_structure_type(self, posts: List[Dict]) -> str:
        """Определяет тип структуры постов."""
        has_numbered = sum(1 for p in posts if re.search(r'^\d+\.', p["content"], re.MULTILINE))
        has_bullet = sum(1 for p in posts if re.search(r'^[-•*]', p["content"], re.MULTILINE))
        has_paragraphs = sum(1 for p in posts if '\n\n' in p["content"])
        
        if has_numbered > len(posts) * 0.3:
            return "numbered_lists"
        elif has_bullet > len(posts) * 0.3:
            return "bullet_lists"
        elif has_paragraphs > len(posts) * 0.5:
            return "paragraphs"
        else:
            return "narrative"
    
    def _detect_topics(self, posts: List[Dict]) -> Dict[str, float]:
        """Определяет тематику постов."""
        all_text = " ".join([p["content"].lower() for p in posts])
        topic_scores = {}
        
        for topic, keywords in self.TOPICS.items():
            matches = sum(1 for keyword in keywords if keyword in all_text)
            topic_scores[topic] = round(matches / len(self.TOPICS[topic]) / max(len(posts), 1) * 100, 2)
        
        return dict(sorted(topic_scores.items(), key=lambda x: x[1], reverse=True))
    
    def _extract_phrases_enhanced(self, posts: List[Dict], max_phrases: int = 7) -> List[str]:
        """Улучшенное извлечение характерных фраз."""
        all_text = " ".join([p["content"] for p in posts])
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        # Биграммы, триграммы и квадриграммы
        ngrams = []
        for n in [2, 3, 4]:
            for i in range(len(words) - n + 1):
                ngrams.append(" ".join(words[i:i+n]))
        
        phrase_counter = Counter(ngrams)
        
        # Улучшенная фильтрация
        filtered_phrases = []
        min_count = max(2, len(posts) // 5)  # Адаптивный минимум
        
        for phrase, count in phrase_counter.most_common(max_phrases * 5):
            # Фильтры
            if phrase.lower() in self.STOP_PHRASES:
                continue
            if len(phrase) < 5:  # Минимум 5 символов
                continue
            if count < min_count:
                continue
            # Проверка на стоп-слова
            words_in_phrase = phrase.split()
            if len(words_in_phrase) < 2:
                continue
            # Проверка на уникальность (не подстрока другой фразы)
            is_substring = any(phrase in fp and phrase != fp for fp in filtered_phrases)
            if is_substring:
                continue
            
            filtered_phrases.append(phrase)
            if len(filtered_phrases) >= max_phrases:
                break
        
        return filtered_phrases
    
    def _get_sample_posts(self, posts: List[Dict], max_samples: int = 5) -> List[str]:
        """Возвращает примеры постов для промпта."""
        if not posts:
            return []
        
        # Выбираем посты средней длины (не самые короткие и не самые длинные)
        sorted_posts = sorted(posts, key=lambda p: len(p["content"]))
        start_idx = len(sorted_posts) // 4
        end_idx = min(start_idx + max_samples, len(sorted_posts))
        
        samples = sorted_posts[start_idx:end_idx]
        return [
            p["content"][:600] + "..." if len(p["content"]) > 600 else p["content"]
            for p in samples
        ]
    
    def clear_cache(self):
        """Очищает кэш."""
        self._cache.clear()

