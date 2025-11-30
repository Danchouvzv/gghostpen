export type SocialNetwork = 'linkedin' | 'instagram' | 'facebook' | 'telegram';

export interface Author {
  id: string;
  name: string;
  profession?: string; // Профессия автора
  role: string;
  avatar: string;
  samplePosts: string[];
  stats: {
    formality: string;
    avgLength: number;
    emojiDensity: string;
  };
  is_demo?: boolean;
  user_id?: string;
}

export interface GenerateRequest {
  author_id?: string;
  user_id?: string;
  social_network: SocialNetwork;
  topic: string;
  sample_posts?: string[];
}

export interface DebugInfo {
  target_length: number;
  model_version: string;
  processing_time_ms: number;
  prompt_tokens: number;
}

export interface GenerateResponse {
  generated_post: string;
  style_similarity: number;
  debug: DebugInfo;
}

export enum AppStatus {
  IDLE = 'idle',
  LOADING = 'loading',
  SUCCESS = 'success',
  ERROR = 'error',
}