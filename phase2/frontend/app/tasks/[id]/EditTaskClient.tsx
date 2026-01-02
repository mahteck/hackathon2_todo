'use client';

import { Task } from '@/lib/types';
import TaskForm from '@/components/TaskForm';
import Link from 'next/link';
import { taskApi } from '@/lib/api';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface EditTaskClientProps {
  task: Task;
}

export default function EditTaskClient({ task }: EditTaskClientProps) {
  const router = useRouter();
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await taskApi.delete(task.id);
      router.push('/');
      router.refresh();
    } catch (error) {
      console.error('Failed to delete task:', error);
      setIsDeleting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <Link
          href="/"
          className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
        >
          <svg
            className="mr-2 h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Back to tasks
        </Link>
        <div className="mt-4 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
            <p className="mt-2 text-sm text-gray-600">
              Update task details or delete it
            </p>
          </div>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="px-4 py-2 text-sm font-medium text-red-700 bg-white border border-red-300 rounded-md hover:bg-red-50"
          >
            Delete Task
          </button>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <TaskForm task={task} />
      </div>

      {/* Delete confirmation modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Delete Task
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              Are you sure you want to delete "{task.title}"? This action cannot be undone.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                disabled={isDeleting}
                className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 disabled:opacity-50"
              >
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
