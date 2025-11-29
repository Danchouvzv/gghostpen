#!/usr/bin/env python3
"""
Скрипт для подготовки и валидации датасета GhostPen.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import jsonschema


def validate_dataset(dataset_path: Path, schema_path: Path) -> bool:
    """
    Валидирует датасет по JSON Schema.
    
    Args:
        dataset_path: Путь к файлу датасета
        schema_path: Путь к файлу схемы
        
    Returns:
        True если валиден, False иначе
    """
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        jsonschema.validate(instance=dataset, schema=schema)
        print("✅ Датасет валиден!")
        return True
    except jsonschema.ValidationError as e:
        print(f"❌ Ошибка валидации: {e.message}")
        print(f"   Путь: {'.'.join(str(x) for x in e.path)}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        return False
    except FileNotFoundError as e:
        print(f"❌ Файл не найден: {e}")
        return False


def get_dataset_stats(dataset_path: Path) -> Dict[str, Any]:
    """
    Собирает статистику по датасету.
    
    Args:
        dataset_path: Путь к файлу датасета
        
    Returns:
        Словарь со статистикой
    """
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    stats = {
        "total_authors": len(dataset["authors"]),
        "total_posts": 0,
        "platforms": {
            "linkedin": 0,
            "instagram": 0,
            "facebook": 0,
            "telegram": 0
        },
        "avg_post_length": 0,
        "authors_details": []
    }
    
    total_length = 0
    
    for author in dataset["authors"]:
        author_stats = {
            "author_id": author["author_id"],
            "total_posts": 0,
            "platforms": {}
        }
        
        for platform, posts in author["platforms"].items():
            count = len(posts)
            stats["platforms"][platform] += count
            stats["total_posts"] += count
            author_stats["total_posts"] += count
            author_stats["platforms"][platform] = count
            
            for post in posts:
                total_length += len(post["content"])
        
        stats["authors_details"].append(author_stats)
    
    if stats["total_posts"] > 0:
        stats["avg_post_length"] = total_length // stats["total_posts"]
    
    return stats


def print_stats(stats: Dict[str, Any]) -> None:
    """Выводит статистику в консоль."""
    print("\n" + "="*50)
    print("📊 СТАТИСТИКА ДАТАСЕТА")
    print("="*50)
    print(f"Авторов: {stats['total_authors']}")
    print(f"Всего постов: {stats['total_posts']}")
    print(f"\nПо платформам:")
    for platform, count in stats['platforms'].items():
        if count > 0:
            print(f"  {platform}: {count}")
    print(f"\nСредняя длина поста: {stats['avg_post_length']} символов")
    print("\nПо авторам:")
    for author in stats['authors_details']:
        print(f"  {author['author_id']}: {author['total_posts']} постов")
        for platform, count in author['platforms'].items():
            if count > 0:
                print(f"    - {platform}: {count}")
    print("="*50 + "\n")


def main():
    """Главная функция."""
    if len(sys.argv) < 2:
        print("Использование: python prepare_dataset.py <команда> [аргументы]")
        print("\nКоманды:")
        print("  validate <dataset.json> <schema.json>  - Валидация датасета")
        print("  stats <dataset.json>                   - Статистика датасета")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "validate":
        if len(sys.argv) < 4:
            print("Ошибка: укажите пути к датасету и схеме")
            sys.exit(1)
        
        dataset_path = Path(sys.argv[2])
        schema_path = Path(sys.argv[3])
        
        if not validate_dataset(dataset_path, schema_path):
            sys.exit(1)
    
    elif command == "stats":
        if len(sys.argv) < 3:
            print("Ошибка: укажите путь к датасету")
            sys.exit(1)
        
        dataset_path = Path(sys.argv[2])
        stats = get_dataset_stats(dataset_path)
        print_stats(stats)
    
    else:
        print(f"Неизвестная команда: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

