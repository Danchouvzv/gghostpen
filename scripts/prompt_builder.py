#!/usr/bin/env python3
"""
Prompt Builder для GhostPen.

Строит идеальные промпты для LLM на основе стилевого профиля автора,
требований платформы и темы поста.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class PromptBuilder:
    """Строитель промптов для генерации постов в авторском стиле."""
    
    # Характеристики платформ
    PLATFORM_RULES = {
        "linkedin": {
            "length": "300-800 символов",
            "tone": "профессиональный, экспертный",
            "structure": "структурированные абзацы, можно использовать списки",
            "emojis": "минимум эмодзи (0-1 на пост)",
            "hashtags": "2-5 хэштегов, профессиональные",
            "style": "формальный, но доступный"
        },
        "instagram": {
            "length": "150-400 символов",
            "tone": "эмоциональный, личный, вдохновляющий",
            "structure": "короткие абзацы, можно использовать эмодзи",
            "emojis": "2-5 эмодзи на пост",
            "hashtags": "3-8 хэштегов, разнообразные",
            "style": "неформальный, живой"
        },
        "facebook": {
            "length": "200-600 символов",
            "tone": "сбалансированный, между формальным и неформальным",
            "structure": "абзацы, можно списки",
            "emojis": "1-3 эмодзи на пост",
            "hashtags": "2-5 хэштегов",
            "style": "универсальный"
        },
        "telegram": {
            "length": "300-1000 символов",
            "tone": "личный, размышляющий, свободный",
            "structure": "длинные абзацы, можно размышления",
            "emojis": "0-2 эмодзи на пост",
            "hashtags": "0-3 хэштега",
            "style": "неформальный, глубокий"
        }
    }
    
    def __init__(self, profiles_path: Optional[Path] = None):
        """
        Инициализация Prompt Builder.
        
        Args:
            profiles_path: Путь к файлу с профилями авторов
        """
        self.profiles = {}
        if profiles_path and profiles_path.exists():
            self.load_profiles(profiles_path)
    
    def load_profiles(self, profiles_path: Path) -> None:
        """Загружает профили авторов."""
        with open(profiles_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for profile in data.get('profiles', []):
                self.profiles[profile['author_id']] = profile
    
    def build_prompt(
        self,
        author_id: str,
        platform: str,
        topic: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Строит промпт для генерации поста.
        
        Args:
            author_id: ID автора
            platform: Платформа (linkedin, instagram, facebook, telegram)
            topic: Тема поста
            additional_context: Дополнительный контекст (опционально)
            
        Returns:
            Готовый промпт для LLM
        """
        if author_id not in self.profiles:
            raise ValueError(f"Профиль автора {author_id} не найден")
        
        profile = self.profiles[author_id]
        platform_rules = self.PLATFORM_RULES.get(platform, self.PLATFORM_RULES["facebook"])
        
        # Строим промпт
        prompt_parts = []
        
        # 1. Основная инструкция
        prompt_parts.append(self._build_main_instruction(profile, platform, topic))
        
        # 2. Стилевые характеристики
        prompt_parts.append(self._build_style_section(profile, platform))
        
        # 3. Примеры постов
        prompt_parts.append(self._build_examples_section(profile))
        
        # 4. Правила платформы
        prompt_parts.append(self._build_platform_rules(platform_rules))
        
        # 5. Тема и контекст
        prompt_parts.append(self._build_topic_section(topic, additional_context))
        
        # 6. Требования к формату
        prompt_parts.append(self._build_format_requirements(profile, platform))
        
        return "\n\n".join(prompt_parts)
    
    def _build_main_instruction(self, profile: Dict, platform: str, topic: str) -> str:
        """Строит основную инструкцию."""
        return f"""Ты пишешь пост в стиле автора {profile['author_id']} для платформы {platform.upper()} на тему "{topic}".

Твоя задача: создать пост, который звучит как настоящий контент этого автора, но подходит под требования платформы."""
    
    def _build_style_section(self, profile: Dict, platform: str) -> str:
        """Строит секцию со стилевыми характеристиками."""
        style = profile.get('style', {})
        platform_style = profile.get('platform_specific', {}).get(platform, {})
        
        # Используем платформо-специфичный стиль, если есть
        if platform_style:
            tone_info = platform_style.get('tone', {})
            dominant_tone = tone_info.get('dominant', 'balanced')
            avg_length = platform_style.get('avg_length', style.get('avg_post_length', 300))
            emoji_density = platform_style.get('emoji_density', 0)
            hashtag_density = platform_style.get('hashtag_density', 0)
        else:
            tone_info = style.get('tone', {})
            dominant_tone = tone_info.get('dominant', 'balanced')
            avg_length = style.get('avg_post_length', 300)
            emoji_density = style.get('emoji_density', 0)
            hashtag_density = style.get('hashtag_density', 0)
        
        structure_type = style.get('structure_type', 'paragraphs')
        emotionality = style.get('emotionality', 0)
        
        style_text = f"""СТИЛЬ АВТОРА:

Тон: {self._describe_tone(dominant_tone, tone_info)}
Длина поста: примерно {avg_length} символов
Структура: {self._describe_structure(structure_type)}
Эмоциональность: {self._describe_emotionality(emotionality)}
Эмодзи: {'использует' if emoji_density > 0.5 else 'редко использует'} ({emoji_density:.1f} на пост в среднем)
Хэштеги: {'использует активно' if hashtag_density > 2 else 'использует умеренно'} ({hashtag_density:.1f} на пост в среднем)"""
        
        # Добавляем характерные фразы
        signature_phrases = profile.get('signature_phrases', [])
        if signature_phrases:
            phrases_text = ", ".join(signature_phrases[:5])
            style_text += f"\nХарактерные фразы автора: {phrases_text}"
        
        return style_text
    
    def _build_examples_section(self, profile: Dict) -> str:
        """Строит секцию с примерами постов."""
        sample_posts = profile.get('sample_posts', [])
        if not sample_posts:
            print(f"⚠️ [PromptBuilder] Нет sample_posts в профиле {profile.get('author_id', 'unknown')}")
            return ""
        
        print(f"✅ [PromptBuilder] Используем {len(sample_posts)} примеров постов для {profile.get('author_id', 'unknown')}")
        
        examples_text = "ПРИМЕРЫ ПОСТОВ ЭТОГО АВТОРА:\n\n"
        for i, post in enumerate(sample_posts[:3], 1):
            # Если post - это словарь, извлекаем content
            if isinstance(post, dict):
                post_content = post.get('content', str(post))
            else:
                post_content = str(post)
            examples_text += f"Пример {i}:\n{post_content}\n\n"
            print(f"   📄 Пример {i} добавлен (длина: {len(post_content)} символов)")
        
        return examples_text.strip()
    
    def _build_platform_rules(self, platform_rules: Dict) -> str:
        """Строит секцию с правилами платформы."""
        return f"""ТРЕБОВАНИЯ ПЛАТФОРМЫ:

Длина: {platform_rules['length']}
Тон: {platform_rules['tone']}
Структура: {platform_rules['structure']}
Эмодзи: {platform_rules['emojis']}
Хэштеги: {platform_rules['hashtags']}
Общий стиль: {platform_rules['style']}"""
    
    def _build_topic_section(self, topic: str, additional_context: Optional[str]) -> str:
        """Строит секцию с темой."""
        topic_text = f"ТЕМА ПОСТА: {topic}"
        if additional_context:
            topic_text += f"\n\nДополнительный контекст: {additional_context}"
        return topic_text
    
    def _build_format_requirements(self, profile: Dict, platform: str) -> str:
        """Строит секцию с требованиями к формату."""
        style = profile.get('style', {})
        uses_lists = style.get('uses_lists', False)
        list_freq = style.get('list_frequency', 0)
        
        format_text = "ТРЕБОВАНИЯ К ФОРМАТУ:\n"
        format_text += "- Пост должен быть на русском языке\n"
        format_text += "- Сохраняй структуру (абзацы, переносы строк)\n"
        
        if uses_lists and list_freq > 0.3:
            format_text += "- Можно использовать нумерованные или маркированные списки\n"
        
        format_text += "- Не добавляй лишних символов или форматирования\n"
        format_text += "- Пост должен звучать естественно и человечно\n"
        format_text += "\nСгенерируй пост, который соответствует всем требованиям выше."
        
        return format_text
    
    def _describe_tone(self, dominant: str, tone_info: Dict) -> str:
        """Описывает тон текста."""
        descriptions = {
            "formal": "формальный, профессиональный",
            "emotional": "эмоциональный, живой",
            "expert": "экспертный, технический",
            "casual": "разговорный, неформальный"
        }
        base = descriptions.get(dominant, "сбалансированный")
        
        # Добавляем дополнительные характеристики
        if tone_info.get('expert', 0) > 5:
            base += ", с элементами экспертизы"
        if tone_info.get('emotional', 0) > 5:
            base += ", с эмоциональной окраской"
        
        return base
    
    def _describe_structure(self, structure_type: str) -> str:
        """Описывает структуру."""
        descriptions = {
            "numbered_lists": "часто использует нумерованные списки",
            "bullet_lists": "часто использует маркированные списки",
            "paragraphs": "структурированные абзацы",
            "narrative": "повествовательный стиль"
        }
        return descriptions.get(structure_type, "абзацы")
    
    def _describe_emotionality(self, score: float) -> str:
        """Описывает эмоциональность."""
        if score < 2:
            return "низкая, сдержанная"
        elif score < 5:
            return "умеренная"
        else:
            return "высокая, выразительная"


def main():
    """Пример использования Prompt Builder."""
    import sys
    
    if len(sys.argv) < 4:
        print("Использование: python prompt_builder.py <profiles.json> <author_id> <platform> <topic>")
        print("\nПример:")
        print("  python prompt_builder.py dataset/author_profiles.json person_01 linkedin 'О важности планирования'")
        sys.exit(1)
    
    profiles_path = Path(sys.argv[1])
    author_id = sys.argv[2]
    platform = sys.argv[3]
    topic = sys.argv[4] if len(sys.argv) > 4 else "О важности планирования"
    
    builder = PromptBuilder(profiles_path)
    
    try:
        prompt = builder.build_prompt(author_id, platform, topic)
        print("=" * 80)
        print("СГЕНЕРИРОВАННЫЙ ПРОМПТ:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

