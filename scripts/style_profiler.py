#!/usr/bin/env python3
"""
Style Profiler для GhostPen.

Анализирует посты авторов из датасета и создаёт стилевые профили,
которые используются для генерации постов в авторском стиле.
"""

import json
import re
import statistics
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import Counter
from datetime import datetime, timezone


class StyleProfiler:
    """Анализатор стиля автора."""
    
    # Словари для определения тона
    FORMAL_WORDS = ['понимаю', 'применяю', 'рекомендую', 'следует', 'необходимо', 
                    'важно', 'ключевой', 'принцип', 'подход', 'методология']
    EMOTIONAL_WORDS = ['чувствую', 'люблю', 'нравится', 'волнуюсь', 'страшно', 
                       'интересно', 'удивительно', 'вдохновляет', 'радует']
    EXPERT_WORDS = ['анализ', 'решение', 'оптимизация', 'архитектура', 'метрики',
                    'стратегия', 'трансформация', 'процесс', 'система']
    CASUAL_WORDS = ['кстати', 'вообще', 'короче', 'типа', 'как бы', 'в общем']
    
    # Расширенный список стоп-фраз для фильтрации signature_phrases
    STOP_PHRASES = {
        # Временные маркеры
        'вчера на', 'сегодня я', 'сегодня утром', 'сегодня вечером', 'на этой неделе',
        'за последние', 'недавно я', 'недавно мы', 'вчера получил', 'сегодня начал',
        # Общие фразы
        'это не', 'это про', 'что вы', 'как вы', 'это значит', 'это то', 'это как',
        'когда мы', 'когда ты', 'когда я', 'если вы', 'если мы', 'если ты',
        'для того', 'для вас', 'для нас', 'для меня', 'для тебя',
        'может быть', 'может быть', 'может быть', 'может быть',
        'всегда есть', 'всегда можно', 'всегда нужно', 'всегда важно',
        'очень важно', 'очень важно', 'очень интересно', 'очень полезно',
        'не только', 'не просто', 'не всегда', 'не обязательно',
        'то есть', 'то есть', 'то есть', 'то есть',
        'так что', 'так что', 'так что', 'так что',
        'и это', 'и это', 'и это', 'и это',
        'но это', 'но это', 'но это', 'но это',
        'или это', 'или это', 'или это', 'или это',
        # Вопросы
        'что думаете', 'что вы думаете', 'как вы думаете', 'что вы',
        'как вы', 'что думаешь', 'как думаешь',
        # Связки
        'а также', 'а также', 'а также', 'а также',
        'и ещё', 'и ещё', 'и ещё', 'и ещё',
        'но и', 'но и', 'но и', 'но и',
    }
    
    # Темы
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
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
    
    def analyze_author(self, author_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует стиль автора на основе всех его постов.
        
        Args:
            author_data: Данные автора из датасета
            
        Returns:
            Стилевой профиль автора
        """
        author_id = author_data["author_id"]
        all_posts = []
        
        # Собираем все посты автора
        for platform, posts in author_data.get("platforms", {}).items():
            for post in posts:
                all_posts.append({
                    "content": post["content"],
                    "platform": platform,
                    "meta": post.get("meta", {})
                })
        
        if not all_posts:
            return self._empty_profile(author_id)
        
        # Анализируем стиль
        profile = {
            "author_id": author_id,
            "generated_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "total_posts": len(all_posts),
            "platforms": list(author_data.get("platforms", {}).keys()),
            "style": self._analyze_style(all_posts),
            "platform_specific": self._analyze_platforms(all_posts),
            "topics": self._detect_topics(all_posts),
            "signature_phrases": self._extract_phrases(all_posts),
            "sample_posts": self._get_sample_posts(all_posts, max_samples=3)
        }
        
        return profile
    
    def _analyze_style(self, posts: List[Dict]) -> Dict[str, Any]:
        """Анализирует общий стиль автора."""
        all_text = " ".join([p["content"] for p in posts])
        sentences = self._split_sentences(all_text)
        
        # Длина
        post_lengths = [len(p["content"]) for p in posts]
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        
        # Структура
        paragraphs_per_post = [p["content"].count("\n\n") + 1 for p in posts]
        has_lists = sum(1 for p in posts if re.search(r'^\d+\.|^[-•]', p["content"], re.MULTILINE))
        
        # Эмодзи и хэштеги
        total_emojis = sum(len(p.get("meta", {}).get("emojis", [])) for p in posts)
        total_hashtags = sum(len(p.get("meta", {}).get("hashtags", [])) for p in posts)
        emoji_density = total_emojis / len(posts) if posts else 0
        hashtag_density = total_hashtags / len(posts) if posts else 0
        
        # Тон
        tone_scores = self._analyze_tone(all_text)
        
        # Эмоциональность
        emotionality = self._calculate_emotionality(all_text)
        
        return {
            "avg_post_length": int(statistics.mean(post_lengths)) if post_lengths else 0,
            "min_post_length": min(post_lengths) if post_lengths else 0,
            "max_post_length": max(post_lengths) if post_lengths else 0,
            "avg_sentence_length": float(statistics.mean(sentence_lengths)) if sentence_lengths else 0,
            "avg_paragraphs_per_post": float(statistics.mean(paragraphs_per_post)) if paragraphs_per_post else 0,
            "uses_lists": has_lists > 0,
            "list_frequency": has_lists / len(posts) if posts else 0,
            "emoji_density": round(emoji_density, 2),
            "hashtag_density": round(hashtag_density, 2),
            "tone": tone_scores,
            "emotionality": round(emotionality, 2),
            "structure_type": self._detect_structure_type(posts)
        }
    
    def _analyze_platforms(self, posts: List[Dict]) -> Dict[str, Any]:
        """Анализирует стиль по платформам."""
        platform_data = {}
        
        for platform in ['linkedin', 'instagram', 'facebook', 'telegram']:
            platform_posts = [p for p in posts if p["platform"] == platform]
            if not platform_posts:
                continue
            
            platform_text = " ".join([p["content"] for p in platform_posts])
            sentences = self._split_sentences(platform_text)
            
            post_lengths = [len(p["content"]) for p in platform_posts]
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            
            total_emojis = sum(len(p.get("meta", {}).get("emojis", [])) for p in platform_posts)
            total_hashtags = sum(len(p.get("meta", {}).get("hashtags", [])) for p in platform_posts)
            
            platform_data[platform] = {
                "post_count": len(platform_posts),
                "avg_length": int(statistics.mean(post_lengths)) if post_lengths else 0,
                "avg_sentence_length": float(statistics.mean(sentence_lengths)) if sentence_lengths else 0,
                "emoji_density": round(total_emojis / len(platform_posts), 2) if platform_posts else 0,
                "hashtag_density": round(total_hashtags / len(platform_posts), 2) if platform_posts else 0,
                "tone": self._analyze_tone(platform_text)
            }
        
        return platform_data
    
    def _analyze_tone(self, text: str) -> Dict[str, float]:
        """Определяет тон текста."""
        text_lower = text.lower()
        
        formal_score = sum(1 for word in self.FORMAL_WORDS if word in text_lower) / max(len(text.split()), 1) * 1000
        emotional_score = sum(1 for word in self.EMOTIONAL_WORDS if word in text_lower) / max(len(text.split()), 1) * 1000
        expert_score = sum(1 for word in self.EXPERT_WORDS if word in text_lower) / max(len(text.split()), 1) * 1000
        casual_score = sum(1 for word in self.CASUAL_WORDS if word in text_lower) / max(len(text.split()), 1) * 1000
        
        # Определяем доминирующий тон
        scores = {
            "formal": round(formal_score, 2),
            "emotional": round(emotional_score, 2),
            "expert": round(expert_score, 2),
            "casual": round(casual_score, 2)
        }
        
        dominant = max(scores.items(), key=lambda x: x[1])[0]
        scores["dominant"] = dominant
        
        return scores
    
    def _calculate_emotionality(self, text: str) -> float:
        """Вычисляет уровень эмоциональности."""
        emotional_words = sum(1 for word in self.EMOTIONAL_WORDS if word in text.lower())
        emojis_count = len(self.emoji_pattern.findall(text))
        exclamation_count = text.count('!')
        question_count = text.count('?')
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        # Нормализованная метрика эмоциональности
        emotionality = (emotional_words * 2 + emojis_count * 3 + exclamation_count + question_count) / total_words * 100
        
        return min(emotionality, 10.0)  # Ограничиваем максимум
    
    def _detect_structure_type(self, posts: List[Dict]) -> str:
        """Определяет тип структуры постов."""
        has_numbered_lists = sum(1 for p in posts if re.search(r'^\d+\.', p["content"], re.MULTILINE))
        has_bullet_lists = sum(1 for p in posts if re.search(r'^[-•]', p["content"], re.MULTILINE))
        has_paragraphs = sum(1 for p in posts if '\n\n' in p["content"])
        
        if has_numbered_lists > len(posts) * 0.3:
            return "numbered_lists"
        elif has_bullet_lists > len(posts) * 0.3:
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
        
        # Сортируем по убыванию
        sorted_topics = dict(sorted(topic_scores.items(), key=lambda x: x[1], reverse=True))
        
        return sorted_topics
    
    def _extract_phrases(self, posts: List[Dict], max_phrases: int = 5) -> List[str]:
        """Извлекает характерные фразы автора."""
        # Ищем часто встречающиеся фразы из 2-3 слов
        all_text = " ".join([p["content"] for p in posts])
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        # Биграммы и триграммы
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
        
        # Считаем частоту
        phrase_counter = Counter(bigrams + trigrams)
        
        # Фильтруем стоп-фразы и слишком частые общие фразы
        filtered_phrases = []
        for phrase, count in phrase_counter.most_common(max_phrases * 3):
            # Пропускаем стоп-фразы
            if phrase.lower() in self.STOP_PHRASES:
                continue
            # Пропускаем слишком короткие (меньше 4 символов)
            if len(phrase) < 4:
                continue
            # Пропускаем фразы только из стоп-слов
            words = phrase.split()
            if len(words) < 2:
                continue
            # Минимум 2 вхождения
            if count < 2:
                continue
            filtered_phrases.append(phrase)
            if len(filtered_phrases) >= max_phrases:
                break
        
        return filtered_phrases
    
    def _get_sample_posts(self, posts: List[Dict], max_samples: int = 3) -> List[str]:
        """Возвращает примеры постов для промпта."""
        # Выбираем посты средней длины (не самые короткие и не самые длинные)
        sorted_posts = sorted(posts, key=lambda p: len(p["content"]))
        start_idx = len(sorted_posts) // 4
        end_idx = start_idx + max_samples
        
        samples = sorted_posts[start_idx:end_idx]
        return [p["content"][:500] + "..." if len(p["content"]) > 500 else p["content"] 
                for p in samples]
    
    def _split_sentences(self, text: str) -> List[str]:
        """Разбивает текст на предложения."""
        # Простое разбиение по знакам препинания
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _empty_profile(self, author_id: str) -> Dict[str, Any]:
        """Возвращает пустой профиль для автора без постов."""
        return {
            "author_id": author_id,
            "generated_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "total_posts": 0,
            "platforms": [],
            "style": {},
            "platform_specific": {},
            "topics": {},
            "signature_phrases": [],
            "sample_posts": []
        }


def generate_profiles(dataset_path: Path, output_path: Path) -> None:
    """
    Генерирует стилевые профили для всех авторов из датасета.
    
    Args:
        dataset_path: Путь к файлу датасета
        output_path: Путь для сохранения профилей
    """
    print(f"📖 Загружаю датасет из {dataset_path}...")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    profiler = StyleProfiler()
    profiles = []
    
    print(f"🔍 Анализирую {len(dataset['authors'])} авторов...")
    for author in dataset['authors']:
        author_id = author['author_id']
        print(f"  → {author_id}...", end=' ', flush=True)
        
        profile = profiler.analyze_author(author)
        profiles.append(profile)
        
        print(f"✓ ({profile['total_posts']} постов)")
    
    result = {
        "version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "profiles": profiles
    }
    
    print(f"\n💾 Сохраняю профили в {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Готово! Создано {len(profiles)} профилей.")


def main():
    """Главная функция."""
    import sys
    
    if len(sys.argv) < 3:
        print("Использование: python style_profiler.py <dataset.json> <output_profiles.json>")
        sys.exit(1)
    
    dataset_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    if not dataset_path.exists():
        print(f"❌ Файл датасета не найден: {dataset_path}")
        sys.exit(1)
    
    generate_profiles(dataset_path, output_path)


if __name__ == "__main__":
    main()

