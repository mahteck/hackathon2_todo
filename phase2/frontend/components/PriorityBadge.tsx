import { Priority } from '@/lib/types';
import { getPriorityColor } from '@/lib/utils';

interface PriorityBadgeProps {
  priority: Priority;
}

export default function PriorityBadge({ priority }: PriorityBadgeProps) {
  const colorClass = getPriorityColor(priority);

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${colorClass}`}
    >
      {priority.toUpperCase()}
    </span>
  );
}
