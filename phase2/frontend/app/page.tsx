import { Suspense } from 'react';
import TaskList from '@/components/TaskList';
import FilterPanel from '@/components/FilterPanel';
import { Priority } from '@/lib/types';

interface HomePageProps {
  searchParams: {
    status?: 'all' | 'active' | 'completed';
    priority?: Priority;
    sort?: string;
  };
}

function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );
}

export default function HomePage({ searchParams }: HomePageProps) {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <p className="mt-2 text-sm text-gray-600">
          Organize and track your tasks efficiently
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Filters sidebar */}
        <div className="lg:col-span-1">
          <FilterPanel />
        </div>

        {/* Task list */}
        <div className="lg:col-span-3">
          <Suspense fallback={<LoadingSpinner />}>
            <TaskList
              status={searchParams.status}
              priority={searchParams.priority}
              sort={searchParams.sort}
            />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
