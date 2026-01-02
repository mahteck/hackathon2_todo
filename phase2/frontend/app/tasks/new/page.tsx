'use client';

import TaskForm from '@/components/TaskForm';
import Link from 'next/link';

export default function NewTaskPage() {
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
        <h1 className="mt-4 text-3xl font-bold text-gray-900">Create New Task</h1>
        <p className="mt-2 text-sm text-gray-600">
          Add a new task to your todo list
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <TaskForm />
      </div>
    </div>
  );
}
