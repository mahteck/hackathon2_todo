'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Task } from '@/lib/types';
import { taskApi } from '@/lib/api';
import PriorityBadge from './PriorityBadge';
import { formatDate, isOverdue } from '@/lib/utils';

interface TaskCardProps {
  task: Task;
  onUpdate?: () => void;
}

export default function TaskCard({ task, onUpdate }: TaskCardProps) {
  const [completed, setCompleted] = useState(task.completed);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggleComplete = async () => {
    setIsUpdating(true);
    const newStatus = !completed;
    setCompleted(newStatus); // Optimistic update

    try {
      await taskApi.update(task.id, { completed: newStatus });
      onUpdate?.();
    } catch (error) {
      setCompleted(!newStatus); // Revert on error
      console.error('Failed to update task:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const taskOverdue = task.due_date && !completed && isOverdue(task.due_date);

  return (
    <div className="bg-white border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={completed}
          onChange={handleToggleComplete}
          disabled={isUpdating}
          className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <Link
              href={`/tasks/${task.id}`}
              className={`text-lg font-medium hover:text-blue-600 ${
                completed ? 'line-through text-gray-500' : 'text-gray-900'
              }`}
            >
              {task.title}
            </Link>
            <PriorityBadge priority={task.priority} />
            {taskOverdue && (
              <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800 border border-red-200">
                Overdue
              </span>
            )}
          </div>

          {task.description && (
            <p className="text-sm text-gray-600 mb-2">{task.description}</p>
          )}

          <div className="flex items-center gap-3 text-sm text-gray-500 flex-wrap">
            {task.due_date && (
              <span className="flex items-center gap-1">
                <svg
                  className="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                {formatDate(task.due_date)}
              </span>
            )}

            {task.tags.length > 0 && (
              <div className="flex gap-1 flex-wrap">
                {task.tags.map((tag) => (
                  <span
                    key={tag.id}
                    className="px-2 py-1 rounded text-xs font-medium"
                    style={{
                      backgroundColor: tag.color ? `${tag.color}20` : '#e5e7eb',
                      color: tag.color || '#374151',
                      border: `1px solid ${tag.color || '#d1d5db'}`,
                    }}
                  >
                    {tag.name}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
