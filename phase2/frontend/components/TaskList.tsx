import { taskApi } from '@/lib/api';
import { FilterParams, Task } from '@/lib/types';
import TaskCard from './TaskCard';

interface TaskListProps extends FilterParams {}

export default async function TaskList(props: TaskListProps) {
  let tasks: Task[] = [];
  let total = 0;
  let error: string | null = null;

  try {
    const response = await taskApi.list(props);
    tasks = response.data.tasks;
    total = response.data.total;
  } catch (err) {
    error = err instanceof Error ? err.message : 'Failed to load tasks';
  }

  if (error) {
    return (
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
        <p className="text-sm text-gray-500 mt-2">
          Make sure the backend server is running at http://localhost:8000
        </p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-100 mb-4">
          <svg
            className="h-6 w-6 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <p className="text-lg">No tasks found</p>
        <p className="text-sm mt-2">Create your first task to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
      <div className="text-sm text-gray-500 text-center mt-4">
        Showing {tasks.length} of {total} tasks
      </div>
    </div>
  );
}
