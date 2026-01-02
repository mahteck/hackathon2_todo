import { Priority } from '@/lib/types';

interface PrioritySelectorProps {
  value: Priority;
  onChange: (priority: Priority) => void;
}

export default function PrioritySelector({ value, onChange }: PrioritySelectorProps) {
  const priorities = [
    { value: Priority.HIGH, label: 'High', color: 'red' },
    { value: Priority.MEDIUM, label: 'Medium', color: 'amber' },
    { value: Priority.LOW, label: 'Low', color: 'blue' },
  ];

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Priority
      </label>
      <div className="grid grid-cols-3 gap-2">
        {priorities.map((priority) => (
          <button
            key={priority.value}
            type="button"
            onClick={() => onChange(priority.value)}
            className={`px-4 py-2 text-sm font-medium rounded-md border transition-colors ${
              value === priority.value
                ? `bg-${priority.color}-100 text-${priority.color}-800 border-${priority.color}-300`
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            }`}
          >
            {priority.label}
          </button>
        ))}
      </div>
    </div>
  );
}
