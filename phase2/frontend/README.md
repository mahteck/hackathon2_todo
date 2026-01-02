# Todo App - Phase II Frontend

Modern, responsive web interface built with Next.js 14, TypeScript, and Tailwind CSS for the Evolution of Todo project.

## Features

- **Next.js 14 App Router** - Latest Next.js with server components
- **TypeScript** - Full type safety throughout the app
- **Tailwind CSS** - Utility-first styling with custom theme
- **Server Components** - Efficient server-side rendering
- **Client Components** - Interactive UI with optimistic updates
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Optimistic UI updates for better UX
- **Filter & Sort** - Advanced filtering and sorting options
- **Tag Management** - Create and manage tags with autocomplete
- **Priority Indicators** - Color-coded priority badges
- **Due Date Tracking** - Overdue detection and date formatting

## Technology Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React Server Components** - Server-side rendering by default
- **date-fns** - Modern JavaScript date utility library

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout with navigation
│   ├── page.tsx                # Home page with task list
│   ├── globals.css             # Global styles
│   ├── tasks/
│   │   ├── new/
│   │   │   └── page.tsx       # Create task page
│   │   └── [id]/
│   │       ├── page.tsx       # Edit task page (server)
│   │       └── EditTaskClient.tsx  # Edit task client component
├── components/
│   ├── Navigation.tsx          # App navigation header
│   ├── TaskCard.tsx            # Task item component (client)
│   ├── TaskList.tsx            # Task list container (server)
│   ├── FilterPanel.tsx         # Filter controls (client)
│   ├── TaskForm.tsx            # Create/edit form (client)
│   ├── PriorityBadge.tsx       # Priority indicator
│   ├── PrioritySelector.tsx    # Priority input
│   ├── DueDatePicker.tsx       # Date picker
│   └── TagInput.tsx            # Tag autocomplete input (client)
├── lib/
│   ├── types.ts                # TypeScript type definitions
│   ├── api.ts                  # API client functions
│   └── utils.ts                # Utility functions
├── public/                     # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
├── .env.local                  # Environment variables
└── README.md
```

## Setup Instructions

### Prerequisites

- Node.js 18+ or higher
- npm or yarn package manager
- Backend API running on http://localhost:8000

### 1. Navigate to Frontend Directory

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2/frontend
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure Environment

Create `.env.local` file (should already exist from setup):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, update the API URL:

```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

## Running the Application

### Development Server

```bash
npm run dev
# or
yarn dev
```

The app will be available at http://localhost:3000

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## Features Walkthrough

### 1. Home Page (Task List)

- View all tasks with real-time updates
- Filter by status (all/active/completed)
- Filter by priority (high/medium/low)
- Sort by various criteria (date, priority, title)
- Click checkbox to mark tasks complete (optimistic update)
- Click task title to edit

### 2. Create New Task

- Navigate to `/tasks/new` or click "New Task" button
- Fill in task details:
  - **Title** (required)
  - **Description** (optional)
  - **Priority** (high/medium/low)
  - **Due Date** (optional datetime picker)
  - **Tags** (autocomplete with existing tags)
- Submit to create task

### 3. Edit Task

- Click on any task title to edit
- Update any field
- Delete task with confirmation modal
- Changes saved immediately

### 4. Tag Management

- Tags auto-complete from existing tags
- Create new tags inline in task form
- Tags display with custom colors
- Remove tags from task

## Component Architecture

### Server Components

- **TaskList** - Fetches tasks on server, efficient rendering
- **page.tsx** (home) - Server-side filtering and data fetching

### Client Components

- **TaskCard** - Interactive checkbox, optimistic updates
- **FilterPanel** - URL-based filter state
- **TaskForm** - Form validation and submission
- **TagInput** - Autocomplete with API integration

### Hybrid Approach

- Server components for initial render and SEO
- Client components for interactivity
- Optimistic updates for better UX

## API Integration

All API calls are type-safe and centralized in `lib/api.ts`:

```typescript
// List tasks with filters
const response = await taskApi.list({ status: 'active', priority: 'high' });

// Create task
await taskApi.create({ title: 'New Task', tags: ['work'] });

// Update task
await taskApi.update(taskId, { completed: true });

// Delete task
await taskApi.delete(taskId);

// List tags
const tags = await tagApi.list();
```

## Styling

### Tailwind Configuration

Custom colors defined in `tailwind.config.ts`:

```typescript
colors: {
  priority: {
    high: '#EF4444',    // Red
    medium: '#F59E0B',  // Amber
    low: '#3B82F6',     // Blue
  },
}
```

### Responsive Design

- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Grid layouts adjust automatically

## Error Handling

- API errors displayed with user-friendly messages
- Network error fallbacks
- Form validation errors
- 404 pages for missing tasks

## Performance Optimizations

- Server components reduce client-side JavaScript
- Optimistic UI updates for instant feedback
- Efficient re-rendering with Next.js caching
- Lazy loading of client components

## Development Workflow

1. Make changes to components or pages
2. Hot reload automatically shows changes
3. Check TypeScript errors: `npm run build`
4. Test in browser at http://localhost:3000

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Environment Variables

Set in Vercel dashboard:

```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### Build Output

```bash
npm run build
```

Static files in `.next/` directory.

## Troubleshooting

### API Connection Errors

- Ensure backend is running on http://localhost:8000
- Check CORS is enabled in backend
- Verify `.env.local` has correct API URL

### TypeScript Errors

```bash
# Type check without building
npx tsc --noEmit
```

### Module Not Found

```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

### Styling Issues

```bash
# Rebuild Tailwind
npm run dev
```

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

## Next Steps

- Add user authentication (Phase III)
- Implement real-time updates with WebSockets
- Add drag-and-drop task reordering
- Implement offline support with service workers
- Add keyboard shortcuts

## License

Part of the Evolution of Todo hackathon project.
