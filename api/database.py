#!/usr/bin/env python3
"""
База данных для GhostPen.

SQLite база для хранения пользователей, их постов и стилевых профилей.
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone


class Database:
    """Управление базой данных GhostPen."""
    
    def __init__(self, db_path: str = "ghostpen.db"):
        self.db_path = Path(db_path)
        self.init_db()
    
    def get_connection(self):
        """Получить соединение с БД."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Инициализация таблиц БД."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица постов пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_posts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                platform TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                hashtags TEXT,  -- JSON array
                mentions TEXT,  -- JSON array
                emojis TEXT,   -- JSON array
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Таблица стилевых профилей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                profile_json TEXT NOT NULL,  -- JSON профиля стиля
                generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # === Users ===
    def create_user(self, user_id: str, email: Optional[str] = None, name: Optional[str] = None) -> bool:
        """Создать пользователя."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (id, email, name) VALUES (?, ?, ?)",
                (user_id, email, name)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Получить пользователя."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    # === Posts ===
    def add_post(self, user_id: str, platform: str, content: str, 
                 timestamp: Optional[str] = None,
                 hashtags: Optional[List[str]] = None,
                 mentions: Optional[List[str]] = None,
                 emojis: Optional[List[str]] = None) -> str:
        """Добавить пост пользователя."""
        import uuid
        post_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_posts 
            (id, user_id, platform, content, timestamp, hashtags, mentions, emojis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post_id,
            user_id,
            platform,
            content,
            timestamp or datetime.now(timezone.utc).isoformat(),
            json.dumps(hashtags or []),
            json.dumps(mentions or []),
            json.dumps(emojis or [])
        ))
        conn.commit()
        conn.close()
        return post_id
    
    def get_user_posts(self, user_id: str, platform: Optional[str] = None) -> List[Dict]:
        """Получить посты пользователя."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if platform:
            cursor.execute(
                "SELECT * FROM user_posts WHERE user_id = ? AND platform = ? ORDER BY timestamp DESC",
                (user_id, platform)
            )
        else:
            cursor.execute(
                "SELECT * FROM user_posts WHERE user_id = ? ORDER BY timestamp DESC",
                (user_id,)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = []
        for row in rows:
            post = dict(row)
            post['hashtags'] = json.loads(post['hashtags'] or '[]')
            post['mentions'] = json.loads(post['mentions'] or '[]')
            post['emojis'] = json.loads(post['emojis'] or '[]')
            posts.append(post)
        
        return posts
    
    def delete_post(self, post_id: str, user_id: str) -> bool:
        """Удалить пост."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM user_posts WHERE id = ? AND user_id = ?",
            (post_id, user_id)
        )
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    
    # === Profiles ===
    def save_profile(self, user_id: str, profile: Dict[str, Any]) -> bool:
        """Сохранить стилевой профиль пользователя."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles (user_id, profile_json, generated_at)
            VALUES (?, ?, ?)
        """, (
            user_id,
            json.dumps(profile, ensure_ascii=False),
            datetime.now(timezone.utc).isoformat()
        ))
        conn.commit()
        conn.close()
        return True
    
    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получить стилевой профиль пользователя."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT profile_json FROM user_profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row['profile_json']) if row else None
    
    def get_user_data_for_profiling(self, user_id: str) -> Dict[str, Any]:
        """Получить данные пользователя в формате для StyleProfiler."""
        posts = self.get_user_posts(user_id)
        
        if not posts:
            return None
        
        # Группируем по платформам
        platforms_data = {}
        for post in posts:
            platform = post['platform']
            if platform not in platforms_data:
                platforms_data[platform] = []
            
            platforms_data[platform].append({
                'post_id': post['id'],
                'content': post['content'],
                'timestamp': post['timestamp'],
                'meta': {
                    'hashtags': post['hashtags'],
                    'mentions': post['mentions'],
                    'emojis': post['emojis']
                }
            })
        
        return {
            'author_id': f"user_{user_id}",
            'platforms': platforms_data
        }

