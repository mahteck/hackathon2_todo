/**
 * TypeScript types matching backend schemas
 */

export enum Priority {
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

export interface Tag {
  id: number;
  name: string;
  color?: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: Priority;
  due_date?: string; // ISO 8601
  tags: Tag[];
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
  user_id: number;
}

export interface TaskCreateInput {
  title: string;
  description?: string;
  priority?: Priority;
  due_date?: string;
  tags?: string[];
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
  priority?: Priority;
  completed?: boolean;
  due_date?: string;
  tags?: string[];
}

export interface TaskListResponse {
  data: {
    tasks: Task[];
    total: number;
    limit: number;
    offset: number;
  };
}

export interface TaskResponse {
  data: Task;
  message?: string;
}

export interface TagResponse {
  data: Tag[];
}

export interface FilterParams {
  status?: 'all' | 'active' | 'completed';
  priority?: Priority;
  tag?: string[];
  sort?: string;
}
