// User type definition
export interface User {
  id: string;
  email: string;
  created_at: string;
}

// Pet type definition
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

// Diary type definition
export interface Diary {
  id: string;
  pet_id: string;
  pet_name?: string;
  title?: string;
  content: string;
  image_url?: string;
  created_at: string;
}

// Paginated response type definition
export interface PaginatedResponse<T> {
  [key: string]: T[];
  total: number;
  pages: number;
  current_page: number;
}