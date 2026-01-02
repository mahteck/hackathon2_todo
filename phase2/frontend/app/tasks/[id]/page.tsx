import { taskApi } from '@/lib/api';
import EditTaskClient from './EditTaskClient';
import Link from 'next/link';

interface EditTaskPageProps {
  params: {
    id: string;
  };
}

export default async function EditTaskPage({ params }: EditTaskPageProps) {
  const taskId = parseInt(params.id);

  let task = null;
  let error = null;

  try {
    const response = await taskApi.get(taskId);
    task = response.data;
  } catch (err) {
    error = err instanceof Error ? err.message : 'Failed to load task';
  }

  if (error) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 mb-4">
            <svg
              className="h-6 w-6 text-red-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <p className="text-lg text-red-600">{error}</p>
          <Link
            href="/"
            className="mt-4 inline-block text-blue-600 hover:text-blue-800"
          >
            Go back to tasks
          </Link>
        </div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <p className="text-lg text-gray-600">Task not found</p>
          <Link
            href="/"
            className="mt-4 inline-block text-blue-600 hover:text-blue-800"
          >
            Go back to tasks
          </Link>
        </div>
      </div>
    );
  }

  return <EditTaskClient task={task} />;
}
