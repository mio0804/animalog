// ユーザー型定義
export interface User {
  id: string;
  email: string;
  created_at: string;
}

// ペット型定義
export interface Pet {
  id: string;
  name: string;
  species?: string;
  breed?: string;
  birth_date?: string;
  description?: string;
  created_at: string;
  diary_count?: number;
}

// 日記型定義
export interface Diary {
  id: string;
  pet_id: string;
  pet_name?: string;
  title?: string;
  content: string;
  image_url?: string;
  created_at: string;
}

// ページネーションレスポンス型定義
export interface PaginatedResponse<T> {
  [key: string]: T[];
  total: number;
  pages: number;
  current_page: number;
}