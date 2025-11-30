#!/usr/bin/env python3
"""
GhostPen Generator — основной модуль генерации постов.

Использует Prompt Builder для создания промптов и LLM для генерации,
затем применяет post-processing для финальной обработки.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Добавляем путь к скриптам для импорта
sys.path.insert(0, str(Path(__file__).parent))
from prompt_builder import PromptBuilder


class PostProcessor:
    """Обработчик сгенерированных постов."""
    
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
    
    def process(
        self,
        text: str,
        target_length: int,
        emoji_density: float,
        hashtag_density: float,
        structure_type: str
    ) -> str:
        """
        Обрабатывает сгенерированный текст.
        
        Args:
            text: Сгенерированный текст
            target_length: Целевая длина
            emoji_density: Плотность эмодзи
            hashtag_density: Плотность хэштегов
            structure_type: Тип структуры
            
        Returns:
            Обработанный текст
        """
        # Убираем лишние пробелы и переносы
        text = self._clean_whitespace(text)
        
        # Корректируем длину
        text = self._adjust_length(text, target_length)
        
        # Убираем повторы
        text = self._remove_repetitions(text)
        
        # Корректируем эмодзи (если нужно)
        text = self._adjust_emojis(text, emoji_density)
        
        # Корректируем структуру
        text = self._adjust_structure(text, structure_type)
        
        return text.strip()
    
    def _clean_whitespace(self, text: str) -> str:
        """Очищает лишние пробелы."""
        # Убираем множественные пробелы
        text = re.sub(r' +', ' ', text)
        # Убираем множественные переносы строк
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Убираем пробелы в начале строк
        text = re.sub(r'\n +', '\n', text)
        return text.strip()
    
    def _adjust_length(self, text: str, target_length: int) -> str:
        """Улучшенная корректировка длины текста."""
        current_length = len(text)
        tolerance = target_length * 0.25  # 25% допуск (увеличено)
        
        if current_length < target_length - tolerance:
            # Текст слишком короткий - оставляем как есть
            return text
        elif current_length > target_length + tolerance:
            # Улучшенное обрезание: по предложениям, сохраняя смысл
            sentences = re.split(r'([.!?]+)', text)
            result = ""
            for i in range(0, len(sentences) - 1, 2):
                if i + 1 < len(sentences):
                    candidate = result + sentences[i] + sentences[i + 1]
                    if len(candidate) <= target_length + tolerance:
                        result = candidate
                    else:
                        # Если добавление предложения превышает лимит, останавливаемся
                        break
            
            # Если результат слишком короткий, берем первые N символов
            if len(result) < target_length * 0.5:
                # Обрезаем по словам, чтобы не обрывать слово
                words = text[:target_length + tolerance].split()
                result = ' '.join(words[:-1]) if len(words) > 1 else text[:target_length]
            
            return result if result else text[:target_length]
        
        return text
    
    def _remove_repetitions(self, text: str) -> str:
        """Улучшенное удаление повторов фраз."""
        sentences = re.split(r'([.!?]+)', text)
        result = []
        seen_phrases = set()
        
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                sentence = (sentences[i] + sentences[i + 1]).strip()
                if not sentence:
                    continue
                
                # Улучшенная проверка на повторы
                words = sentence.lower().split()
                if len(words) < 3:  # Слишком короткие предложения пропускаем
                    result.append(sentence)
                    continue
                
                # Проверяем первые 6 слов и последние 3
                phrase_key_start = ' '.join(words[:6])
                phrase_key_end = ' '.join(words[-3:]) if len(words) > 3 else ''
                
                # Проверяем на похожесть (не точное совпадение)
                is_repetition = False
                for seen in seen_phrases:
                    if phrase_key_start in seen or seen in phrase_key_start:
                        if len(sentence) > 30:  # Длинные предложения проверяем строже
                            is_repetition = True
                            break
                
                if not is_repetition:
                    result.append(sentence)
                    seen_phrases.add(phrase_key_start)
                    if phrase_key_end:
                        seen_phrases.add(phrase_key_end)
        
        return ' '.join(result) if result else text
    
    def _adjust_emojis(self, text: str, target_density: float) -> str:
        """Корректирует количество эмодзи."""
        emojis = self.emoji_pattern.findall(text)
        current_count = len(emojis)
        target_count = int(target_density)
        
        if current_count > target_count + 1:
            # Убираем лишние эмодзи (оставляем первые)
            emoji_positions = []
            for match in self.emoji_pattern.finditer(text):
                emoji_positions.append((match.start(), match.end()))
            
            # Удаляем эмодзи, начиная с конца
            for start, end in reversed(emoji_positions[target_count:]):
                text = text[:start] + text[end:]
        
        return text
    
    def _adjust_structure(self, text: str, structure_type: str) -> str:
        """Корректирует структуру текста."""
        # Убеждаемся, что есть абзацы
        if '\n\n' not in text and len(text) > 200:
            # Разбиваем по предложениям и создаём абзацы
            sentences = re.split(r'([.!?]+)', text)
            paragraphs = []
            current_para = []
            
            for i in range(0, len(sentences) - 1, 2):
                if i + 1 < len(sentences):
                    sentence = (sentences[i] + sentences[i + 1]).strip()
                    current_para.append(sentence)
                    # Каждые 2-3 предложения - новый абзац
                    if len(current_para) >= 2:
                        paragraphs.append(' '.join(current_para))
                        current_para = []
            
            if current_para:
                paragraphs.append(' '.join(current_para))
            
            if paragraphs:
                return '\n\n'.join(paragraphs)
        
        return text


class LLMInterface:
    """Интерфейс для работы с LLM."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Инициализация LLM интерфейса.
        
        Args:
            api_key: API ключ (если None, используется mock)
            model: Модель для использования
        """
        self.api_key = api_key
        self.model = model
        self.use_mock = api_key is None
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Генерирует текст по промпту.
        
        Args:
            prompt: Промпт для генерации
            max_tokens: Максимальное количество токенов
            
        Returns:
            Сгенерированный текст
        """
        if self.use_mock:
            print("⚠️ [LLM] Используется MOCK генерация (API ключ не установлен)")
            return self._mock_generate(prompt)
        else:
            print(f"✅ [LLM] Используется реальный OpenAI API (ключ: {self.api_key[:10]}...)")
            try:
                result = self._openai_generate(prompt, max_tokens)
                print(f"✅ [LLM] Генерация успешна, длина: {len(result)} символов")
                return result
            except Exception as e:
                print(f"❌ [LLM] Ошибка OpenAI API: {e}")
                print("⚠️ [LLM] Переключаемся на mock генерацию")
                return self._mock_generate(prompt)
    
    def _mock_generate(self, prompt: str) -> str:
        """Mock генерация для тестирования - извлекает тему и генерирует текст."""
        import re
        
        # Извлекаем тему из промпта (несколько вариантов паттернов)
        topic = None
        patterns = [
            r'ТЕМА ПОСТА:\s*(.+?)(?:\n\n|$)',
            r'на тему\s+"(.+?)"',
            r'на тему\s+(.+?)(?:\n|$)',
            r'тема:\s*(.+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE | re.MULTILINE)
            if match:
                topic = match.group(1).strip()
                break
        
        if not topic:
            # Пробуем найти тему в основной инструкции
            main_match = re.search(r'на тему\s+"?([^"]+)"?', prompt, re.IGNORECASE)
            if main_match:
                topic = main_match.group(1).strip()
        
        if not topic:
            topic = "важной теме"
        
        # Убираем кавычки если есть
        topic = topic.strip('"\'')
        
        # Извлекаем стиль автора
        tone_match = re.search(r'Тон:\s*(.+?)(?:\n|$)', prompt, re.IGNORECASE | re.MULTILINE)
        tone_text = tone_match.group(1).strip() if tone_match else ""
        is_formal = "формальный" in tone_text.lower() or "профессиональный" in tone_text.lower()
        is_emotional = "эмоциональный" in tone_text.lower()
        
        # Определяем структуру
        has_lists = "списки" in prompt.lower() or "numbered_lists" in prompt.lower() or "uses_lists" in prompt.lower()
        
        # Определяем платформу
        platform = "linkedin"
        if "instagram" in prompt.lower():
            platform = "instagram"
        elif "telegram" in prompt.lower():
            platform = "telegram"
        elif "facebook" in prompt.lower():
            platform = "facebook"
        
        # Генерируем текст на основе темы, стиля и платформы
        if platform == "instagram" and is_emotional:
            return f"""Сегодня хочу поделиться мыслями о {topic.lower()} ✨

Это действительно важная тема, которая меня вдохновляет! 🌿

Когда я начинаю разбираться в деталях, открываются новые возможности. Это не про быстрые решения, а про глубокое понимание.

Что вы думаете об этом? 💭"""
        
        elif platform == "telegram":
            return f"""⚡️ Быстрые мысли о {topic.lower()}

Честно говоря, я думаю, что многие люди подходят к этому неправильно. {topic} — это не просто концепция, а реальный инструмент.

Когда мы начинаем применять это на практике, открываются интересные возможности. Важно не останавливаться на теории.

Что вы об этом думаете?"""
        
        elif has_lists:
            return f"""Сегодня хочу поделиться мыслями о {topic.lower()}.

За последние годы я понял, что это действительно важная тема, которая требует внимания и системного подхода.

Ключевые моменты:

1. Первый важный аспект связан с пониманием основ и принципов
2. Второй момент — это практическое применение в реальных условиях
3. Третий элемент — постоянное развитие и улучшение подхода

{topic} — это не просто концепция, а реальный инструмент для достижения целей. Важно применять это системно."""
        
        else:
            intro = "Сегодня хочу поделиться мыслями" if is_formal else "Хочу поделиться мыслями"
            return f"""{intro} о {topic.lower()}.

За последние годы я понял, что это действительно важная тема. Когда мы начинаем разбираться в деталях, открываются новые возможности и перспективы.

Важно понимать, что {topic.lower()} требует системного подхода. Это не про быстрые решения, а про глубокое понимание процессов и механизмов.

Что вы думаете об этом?"""
    
    def _openai_generate(self, prompt: str, max_tokens: int) -> str:
        """Генерация через OpenAI API."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты эксперт по созданию контента для социальных сетей."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except ImportError:
            print("⚠️  OpenAI не установлен, используется mock")
            return self._mock_generate(prompt)
        except Exception as e:
            print(f"⚠️  Ошибка при генерации: {e}, используется mock")
            return self._mock_generate(prompt)


class GhostPenGenerator:
    """Основной генератор постов GhostPen."""
    
    def __init__(
        self,
        profiles_path: Path,
        llm_api_key: Optional[str] = None,
        llm_model: str = "gpt-3.5-turbo"
    ):
        """
        Инициализация генератора.
        
        Args:
            profiles_path: Путь к файлу с профилями
            llm_api_key: API ключ для LLM (опционально)
            llm_model: Модель LLM
        """
        self.prompt_builder = PromptBuilder(profiles_path)
        self.llm = LLMInterface(llm_api_key, llm_model)
        self.processor = PostProcessor()
    
    def generate_post(
        self,
        author_id: str,
        platform: str,
        topic: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Генерирует пост в стиле автора.
        
        Args:
            author_id: ID автора
            platform: Платформа
            topic: Тема поста
            additional_context: Дополнительный контекст
            
        Returns:
            Словарь с результатом генерации
        """
        # 1. Строим промпт
        prompt = self.prompt_builder.build_prompt(
            author_id, platform, topic, additional_context
        )
        
        # 2. Получаем профиль для параметров обработки
        profile = self.prompt_builder.profiles[author_id]
        style = profile.get('style', {})
        platform_style = profile.get('platform_specific', {}).get(platform, {})
        
        target_length = platform_style.get('avg_length', style.get('avg_post_length', 300))
        emoji_density = platform_style.get('emoji_density', style.get('emoji_density', 0))
        hashtag_density = platform_style.get('hashtag_density', style.get('hashtag_density', 0))
        structure_type = style.get('structure_type', 'paragraphs')
        
        # 3. Генерируем через LLM
        raw_text = self.llm.generate(prompt, max_tokens=500)
        
        # 4. Обрабатываем результат
        processed_text = self.processor.process(
            raw_text,
            target_length,
            emoji_density,
            hashtag_density,
            structure_type
        )
        
        return {
            "author_id": author_id,
            "platform": platform,
            "topic": topic,
            "generated_post": processed_text,
            "raw_post": raw_text,
            "prompt_used": prompt,
            "metrics": {
                "length": len(processed_text),
                "target_length": target_length,
                "length_match": abs(len(processed_text) - target_length) / target_length < 0.3
            }
        }


def main():
    """Пример использования генератора."""
    import sys
    
    if len(sys.argv) < 4:
        print("Использование: python ghostpen_generator.py <profiles.json> <author_id> <platform> <topic> [api_key]")
        print("\nПример:")
        print("  python ghostpen_generator.py dataset/author_profiles.json person_01 linkedin 'О важности планирования'")
        sys.exit(1)
    
    profiles_path = Path(sys.argv[1])
    author_id = sys.argv[2]
    platform = sys.argv[3]
    topic = sys.argv[4] if len(sys.argv) > 4 else "О важности планирования"
    api_key = sys.argv[5] if len(sys.argv) > 5 else None
    
    generator = GhostPenGenerator(profiles_path, api_key)
    
    try:
        result = generator.generate_post(author_id, platform, topic)
        
        print("=" * 80)
        print("СГЕНЕРИРОВАННЫЙ ПОСТ:")
        print("=" * 80)
        print(result["generated_post"])
        print("=" * 80)
        print(f"\nДлина: {result['metrics']['length']} символов (цель: {result['metrics']['target_length']})")
        print(f"Соответствие длине: {'✓' if result['metrics']['length_match'] else '✗'}")
    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

