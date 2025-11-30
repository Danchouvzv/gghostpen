import { GenerateRequest, GenerateResponse } from '../types';

// URL бэкенда (можно вынести в .env)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Генерирует пост через GhostPen API
 */
export const generatePost = async (request: GenerateRequest): Promise<GenerateResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data: GenerateResponse = await response.json();
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Получает список доступных авторов
 */
export const getAuthors = async (userId?: string) => {
  try {
    const url = userId 
      ? `${API_BASE_URL}/api/authors?user_id=${userId}`
      : `${API_BASE_URL}/api/authors`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Проверка здоровья API
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return await response.json();
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'unhealthy' };
  }
};

/**
 * Регистрация пользователя
 */
export const register = async (name: string, email: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Registration Error:', error);
    throw error;
  }
};

/**
 * Получить информацию о пользователе
 */
export const getUser = async (userId: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/users/${userId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Get User Error:', error);
    throw error;
  }
};

/**
 * Добавить пост пользователя
 */
export const addPost = async (userId: string, post: {
  platform: string;
  content: string;
  timestamp?: string;
  hashtags?: string[];
  mentions?: string[];
  emojis?: string[];
}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/users/${userId}/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(post),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Add Post Error:', error);
    throw error;
  }
};

/**
 * Получить посты пользователя
 */
export const getUserPosts = async (userId: string, platform?: string) => {
  try {
    const url = platform 
      ? `${API_BASE_URL}/api/users/${userId}/posts?platform=${platform}`
      : `${API_BASE_URL}/api/users/${userId}/posts`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Get Posts Error:', error);
    throw error;
  }
};

/**
 * Удалить пост
 */
export const deletePost = async (userId: string, postId: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/users/${userId}/posts/${postId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Delete Post Error:', error);
    throw error;
  }
};

/**
 * Перестроить стилевой профиль
 */
export const rebuildProfile = async (userId: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/users/${userId}/rebuild-profile`, {
      method: 'POST',
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Rebuild Profile Error:', error);
    throw error;
  }
};

