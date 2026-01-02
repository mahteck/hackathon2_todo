/**
 * Type-safe API client for backend communication
 */

import {
  Task,
  TaskCreateInput,
  TaskUpdateInput,
  TaskListResponse,
  TaskResponse,
  FilterParams,
  Tag,
  TagResponse,
} from './types';

// For server-side (Docker): use backend service name
// For client-side (Browser): use localhost or NEXT_PUBLIC_API_URL
const isServer = typeof window === 'undefined';
const API_BASE_URL = isServer
  ? (process.env.INTERNAL_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000')
  : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

export class ApiError extends Error {
  constructor(public status: number, message: string, public details?: any) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      let errorMessage = 'An error occurred';
      let errorDetails = null;

      try {
        const errorData = await response.json();
        errorMessage = errorData.error?.message || errorData.detail || errorMessage;
        errorDetails = errorData.error?.details || errorData.detail;
      } catch {
        // If error response is not JSON, use status text
        errorMessage = response.statusText || errorMessage;
      }

      throw new ApiError(response.status, errorMessage, errorDetails);
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network errors, etc.
    throw new ApiError(0, error instanceof Error ? error.message : 'Network error');
  }
}

// Task API functions
export const taskApi = {
  list: (params: FilterParams = {}) => {
    const searchParams = new URLSearchParams();
    if (params.status) searchParams.set('status', params.status);
    if (params.priority) searchParams.set('priority', params.priority);
    if (params.tag) params.tag.forEach(t => searchParams.append('tag', t));
    if (params.sort) searchParams.set('sort', params.sort);

    const query = searchParams.toString();
    return fetchAPI<TaskListResponse>(
      `/api/v1/tasks${query ? `?${query}` : ''}`
    );
  },

  get: (id: number) =>
    fetchAPI<TaskResponse>(`/api/v1/tasks/${id}`),

  create: (data: TaskCreateInput) =>
    fetchAPI<TaskResponse>('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: TaskUpdateInput) =>
    fetchAPI<TaskResponse>(`/api/v1/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    fetchAPI<{ data: null; message: string }>(`/api/v1/tasks/${id}`, {
      method: 'DELETE',
    }),
};

// Tag API functions
export const tagApi = {
  list: () =>
    fetchAPI<TagResponse>('/api/v1/tags'),

  create: (data: { name: string; color?: string }) =>
    fetchAPI<{ data: Tag; message: string }>('/api/v1/tags', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
