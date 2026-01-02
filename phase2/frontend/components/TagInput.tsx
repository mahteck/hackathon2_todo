'use client';

import { useState, useEffect } from 'react';
import { tagApi } from '@/lib/api';
import { Tag } from '@/lib/types';

interface TagInputProps {
  value: string[];
  onChange: (tags: string[]) => void;
}

export default function TagInput({ value, onChange }: TagInputProps) {
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    // Fetch available tags
    const fetchTags = async () => {
      try {
        const response = await tagApi.list();
        setAvailableTags(response.data);
      } catch (error) {
        console.error('Failed to fetch tags:', error);
      }
    };
    fetchTags();
  }, []);

  const suggestions = availableTags
    .filter((tag) =>
      tag.name.toLowerCase().includes(inputValue.toLowerCase()) &&
      !value.includes(tag.name)
    )
    .slice(0, 5);

  const addTag = (tagName: string) => {
    if (tagName && !value.includes(tagName.toLowerCase())) {
      onChange([...value, tagName.toLowerCase()]);
      setInputValue('');
      setShowSuggestions(false);
    }
  };

  const removeTag = (tagName: string) => {
    onChange(value.filter((t) => t !== tagName));
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      e.preventDefault();
      addTag(inputValue.trim());
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Tags
      </label>

      {/* Selected tags */}
      <div className="flex flex-wrap gap-2 mb-2">
        {value.map((tag) => {
          const tagData = availableTags.find((t) => t.name === tag);
          return (
            <span
              key={tag}
              className="inline-flex items-center px-2.5 py-1 rounded text-sm font-medium"
              style={{
                backgroundColor: tagData?.color ? `${tagData.color}20` : '#e5e7eb',
                color: tagData?.color || '#374151',
                border: `1px solid ${tagData?.color || '#d1d5db'}`,
              }}
            >
              {tag}
              <button
                type="button"
                onClick={() => removeTag(tag)}
                className="ml-1.5 inline-flex items-center justify-center hover:opacity-70"
              >
                <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </span>
          );
        })}
      </div>

      {/* Input */}
      <div className="relative">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            setShowSuggestions(true);
          }}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          onKeyDown={handleKeyDown}
          placeholder="Type to add or search tags..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />

        {/* Suggestions dropdown */}
        {showSuggestions && inputValue && suggestions.length > 0 && (
          <div className="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md border border-gray-200">
            {suggestions.map((tag) => (
              <button
                key={tag.id}
                type="button"
                onClick={() => addTag(tag.name)}
                className="w-full text-left px-3 py-2 hover:bg-gray-50 first:rounded-t-md last:rounded-b-md"
              >
                <span
                  className="inline-block w-3 h-3 rounded-full mr-2"
                  style={{ backgroundColor: tag.color || '#9ca3af' }}
                />
                {tag.name}
              </button>
            ))}
          </div>
        )}
      </div>

      <p className="mt-1 text-sm text-gray-500">
        Press Enter to add a tag
      </p>
    </div>
  );
}
