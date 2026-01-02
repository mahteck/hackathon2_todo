interface DueDatePickerProps {
  value?: string;
  onChange: (value: string | undefined) => void;
}

export default function DueDatePicker({ value, onChange }: DueDatePickerProps) {
  const handleClear = () => {
    onChange(undefined);
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Due Date (Optional)
      </label>
      <div className="flex gap-2">
        <input
          type="datetime-local"
          value={value ? value.slice(0, 16) : ''}
          onChange={(e) => onChange(e.target.value ? new Date(e.target.value).toISOString() : undefined)}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
        {value && (
          <button
            type="button"
            onClick={handleClear}
            className="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Clear
          </button>
        )}
      </div>
    </div>
  );
}
