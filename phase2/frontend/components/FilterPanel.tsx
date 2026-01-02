'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Priority } from '@/lib/types';

export default function FilterPanel() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const currentStatus = searchParams.get('status') || 'all';
  const currentPriority = searchParams.get('priority') || '';
  const currentSort = searchParams.get('sort') || 'created_desc';

  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    router.push(`/?${params.toString()}`);
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <h3 className="text-sm font-medium text-gray-700 mb-3">Filters</h3>

      <div className="space-y-4">
        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <div className="flex gap-2">
            {['all', 'active', 'completed'].map((status) => (
              <button
                key={status}
                onClick={() => updateFilter('status', status === 'all' ? '' : status)}
                className={`px-3 py-1.5 text-sm rounded-md font-medium transition-colors ${
                  currentStatus === status
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Priority Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Priority
          </label>
          <select
            value={currentPriority}
            onChange={(e) => updateFilter('priority', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">All Priorities</option>
            <option value={Priority.HIGH}>High</option>
            <option value={Priority.MEDIUM}>Medium</option>
            <option value={Priority.LOW}>Low</option>
          </select>
        </div>

        {/* Sort Order */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sort By
          </label>
          <select
            value={currentSort}
            onChange={(e) => updateFilter('sort', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="created_desc">Newest First</option>
            <option value="created_asc">Oldest First</option>
            <option value="priority_desc">Priority (High to Low)</option>
            <option value="due_asc">Due Date (Soonest)</option>
            <option value="title_asc">Title (A-Z)</option>
          </select>
        </div>
      </div>
    </div>
  );
}
