#!/usr/bin/env python3
"""
Style Scorer для GhostPen.

Оценивает similarity сгенерированного поста к стилю автора
через embeddings и метрики стиля.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
import statistics


class StyleScorer:
    """Оценщик стилевого сходства."""
    
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
    
    def score(
        self,
        generated_post: str,
        author_profile: Dict[str, Any],
        platform: str
    ) -> Dict[str, float]:
        """
        Оценивает сходство сгенерированного поста со стилем автора.
        
        Args:
            generated_post: Сгенерированный пост
            author_profile: Профиль автора
            platform: Платформа
            
        Returns:
            Словарь с метриками оценки
        """
        style = author_profile.get('style', {})
        platform_style = author_profile.get('platform_specific', {}).get(platform, {})
        
        # Используем платформо-специфичный стиль, если есть
        target_style = platform_style if platform_style else style
        
        scores = {}
        
        # 1. Length Accuracy
        scores['length_accuracy'] = self._score_length(
            generated_post,
            target_style.get('avg_length', style.get('avg_post_length', 300))
        )
        
        # 2. Sentence Length Match
        scores['sentence_length_match'] = self._score_sentence_length(
            generated_post,
            target_style.get('avg_sentence_length', style.get('avg_sentence_length', 10))
        )
        
        # 3. Emoji Density Match
        scores['emoji_density_match'] = self._score_emoji_density(
            generated_post,
            target_style.get('emoji_density', style.get('emoji_density', 0))
        )
        
        # 4. Hashtag Density Match
        scores['hashtag_density_match'] = self._score_hashtag_density(
            generated_post,
            target_style.get('hashtag_density', style.get('hashtag_density', 0))
        )
        
        # 5. Structure Match
        scores['structure_match'] = self._score_structure(
            generated_post,
            style.get('structure_type', 'paragraphs'),
            style.get('uses_lists', False)
        )
        
        # 6. Tone Match (упрощённая версия)
        scores['tone_match'] = self._score_tone(
            generated_post,
            target_style.get('tone', {}).get('dominant', 'balanced')
        )
        
        # 7. Emotionality Match
        scores['emotionality_match'] = self._score_emotionality(
            generated_post,
            style.get('emotionality', 0)
        )
        
        # Общий score (среднее взвешенное)
        weights = {
            'length_accuracy': 0.2,
            'sentence_length_match': 0.15,
            'emoji_density_match': 0.1,
            'hashtag_density_match': 0.1,
            'structure_match': 0.15,
            'tone_match': 0.2,
            'emotionality_match': 0.1
        }
        
        scores['overall_score'] = sum(
            scores[key] * weights.get(key, 0) 
            for key in scores.keys() 
            if key != 'overall_score'
        )
        
        return scores
    
    def _score_length(self, text: str, target_length: int) -> float:
        """Оценивает соответствие длины."""
        current_length = len(text)
        if target_length == 0:
            return 1.0
        
        ratio = current_length / target_length
        # Идеальное соотношение: 0.8 - 1.2
        if 0.8 <= ratio <= 1.2:
            return 1.0
        elif 0.6 <= ratio < 0.8 or 1.2 < ratio <= 1.5:
            return 0.7
        elif 0.4 <= ratio < 0.6 or 1.5 < ratio <= 2.0:
            return 0.4
        else:
            return 0.1
    
    def _score_sentence_length(self, text: str, target_avg: float) -> float:
        """Оценивает соответствие длины предложений."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences or target_avg == 0:
            return 0.5
        
        lengths = [len(s.split()) for s in sentences]
        avg_length = statistics.mean(lengths) if lengths else 0
        
        if target_avg == 0:
            return 0.5
        
        ratio = avg_length / target_avg
        if 0.7 <= ratio <= 1.3:
            return 1.0
        elif 0.5 <= ratio < 0.7 or 1.3 < ratio <= 1.6:
            return 0.7
        else:
            return 0.4
    
    def _score_emoji_density(self, text: str, target_density: float) -> float:
        """Оценивает соответствие плотности эмодзи."""
        emojis = self.emoji_pattern.findall(text)
        current_count = len(emojis)
        
        # Нормализуем на длину текста (примерно)
        text_length = len(text.split())
        if text_length == 0:
            return 0.5
        
        current_density = current_count / text_length * 100 if text_length > 0 else 0
        
        if target_density == 0:
            # Если автор не использует эмодзи, текущее должно быть близко к 0
            return 1.0 if current_density < 0.5 else 0.3
        
        ratio = current_density / target_density if target_density > 0 else 0
        if 0.5 <= ratio <= 1.5:
            return 1.0
        elif 0.3 <= ratio < 0.5 or 1.5 < ratio <= 2.0:
            return 0.7
        else:
            return 0.3
    
    def _score_hashtag_density(self, text: str, target_density: float) -> float:
        """Оценивает соответствие плотности хэштегов."""
        hashtags = re.findall(r'#\w+', text)
        current_count = len(hashtags)
        
        text_length = len(text.split())
        if text_length == 0:
            return 0.5
        
        current_density = current_count / text_length * 100 if text_length > 0 else 0
        
        if target_density == 0:
            return 1.0 if current_density < 0.5 else 0.3
        
        ratio = current_density / target_density if target_density > 0 else 0
        if 0.5 <= ratio <= 1.5:
            return 1.0
        elif 0.3 <= ratio < 0.5 or 1.5 < ratio <= 2.0:
            return 0.7
        else:
            return 0.3
    
    def _score_structure(self, text: str, structure_type: str, uses_lists: bool) -> float:
        """Оценивает соответствие структуры."""
        score = 0.5  # Базовый score
        
        # Проверяем наличие абзацев
        has_paragraphs = '\n\n' in text or text.count('\n') >= 2
        if structure_type in ['paragraphs', 'numbered_lists', 'bullet_lists']:
            if has_paragraphs:
                score += 0.3
        
        # Проверяем наличие списков
        if uses_lists:
            has_numbered = bool(re.search(r'^\d+\.', text, re.MULTILINE))
            has_bullets = bool(re.search(r'^[-•]', text, re.MULTILINE))
            if structure_type == 'numbered_lists' and has_numbered:
                score += 0.2
            elif structure_type == 'bullet_lists' and has_bullets:
                score += 0.2
        else:
            # Если автор не использует списки, их не должно быть
            has_any_lists = bool(re.search(r'^\d+\.|^[-•]', text, re.MULTILINE))
            if not has_any_lists:
                score += 0.2
        
        return min(score, 1.0)
    
    def _score_tone(self, text: str, target_tone: str) -> float:
        """Упрощённая оценка тона (можно улучшить через embeddings)."""
        text_lower = text.lower()
        
        # Простые маркеры тона
        formal_markers = ['важно', 'ключевой', 'принцип', 'подход', 'рекомендую']
        emotional_markers = ['чувствую', 'люблю', 'интересно', 'вдохновляет', 'радует']
        expert_markers = ['анализ', 'решение', 'оптимизация', 'стратегия', 'процесс']
        casual_markers = ['кстати', 'вообще', 'короче', 'типа']
        
        scores = {
            'formal': sum(1 for m in formal_markers if m in text_lower),
            'emotional': sum(1 for m in emotional_markers if m in text_lower),
            'expert': sum(1 for m in expert_markers if m in text_lower),
            'casual': sum(1 for m in casual_markers if m in text_lower)
        }
        
        # Определяем доминирующий тон в тексте
        detected_tone = max(scores.items(), key=lambda x: x[1])[0] if scores else 'balanced'
        
        # Оценка: 1.0 если совпадает, 0.5 если близко, 0.2 если не совпадает
        if detected_tone == target_tone:
            return 1.0
        elif target_tone == 'balanced':
            return 0.7
        else:
            return 0.3
    
    def _score_emotionality(self, text: str, target_emotionality: float) -> float:
        """Оценивает соответствие эмоциональности."""
        emotional_words = ['чувствую', 'люблю', 'нравится', 'волнуюсь', 'страшно',
                          'интересно', 'удивительно', 'вдохновляет', 'радует']
        emojis_count = len(self.emoji_pattern.findall(text))
        exclamation_count = text.count('!')
        question_count = text.count('?')
        
        text_words = len(text.split())
        if text_words == 0:
            return 0.5
        
        emotional_words_count = sum(1 for word in emotional_words if word in text.lower())
        current_emotionality = (emotional_words_count * 2 + emojis_count * 3 + 
                                 exclamation_count + question_count) / text_words * 100
        
        if target_emotionality == 0:
            return 1.0 if current_emotionality < 2 else 0.5
        
        ratio = current_emotionality / target_emotionality if target_emotionality > 0 else 0
        if 0.7 <= ratio <= 1.3:
            return 1.0
        elif 0.5 <= ratio < 0.7 or 1.3 < ratio <= 1.6:
            return 0.7
        else:
            return 0.4


def main():
    """Пример использования scorer."""
    import sys
    
    if len(sys.argv) < 4:
        print("Использование: python style_scorer.py <profiles.json> <author_id> <platform> <generated_post.txt>")
        sys.exit(1)
    
    profiles_path = Path(sys.argv[1])
    author_id = sys.argv[2]
    platform = sys.argv[3]
    post_path = Path(sys.argv[4])
    
    # Загружаем профиль
    with open(profiles_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        profile = next((p for p in data['profiles'] if p['author_id'] == author_id), None)
    
    if not profile:
        print(f"❌ Профиль автора {author_id} не найден")
        sys.exit(1)
    
    # Загружаем сгенерированный пост
    with open(post_path, 'r', encoding='utf-8') as f:
        generated_post = f.read()
    
    # Оцениваем
    scorer = StyleScorer()
    scores = scorer.score(generated_post, profile, platform)
    
    print("=" * 80)
    print("ОЦЕНКА СТИЛЕВОГО СХОДСТВА")
    print("=" * 80)
    for metric, score in scores.items():
        bar = "█" * int(score * 20)
        print(f"{metric:25s}: {score:.3f} {bar}")
    print("=" * 80)
    print(f"\nОбщий score: {scores['overall_score']:.3f}")


if __name__ == "__main__":
    main()

