# Phase III Specification: AI-Powered Todo Chatbot

## Constitution

### Vision
Transform the Evolution of Todo application into an intelligent conversational interface that allows users to manage their tasks through natural language, making task management as simple as talking to a personal assistant.

### Core Principles

1. **Natural Language First**: Users should interact with their todos using conversational language, not memorize commands or syntax.

2. **Intent-Driven Architecture**: The system interprets user intent and maps it to appropriate backend operations, handling ambiguity gracefully.

3. **Context Awareness**: The chatbot maintains awareness of the user's current tasks, priorities, and patterns to provide intelligent responses.

4. **Explicit Confirmations**: Destructive or bulk operations require user confirmation to prevent accidental data loss.

5. **Graceful Degradation**: When uncertain, the chatbot asks clarifying questions rather than making assumptions.

6. **Extensibility**: The architecture supports adding new capabilities and tools without redesigning the core system.

---

## Technical Specification

### 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Chat Client / CLI)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenAI Agents SDK                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Conversational Agent                     │   │
│  │  - Intent Recognition                                 │   │
│  │  - Context Management                                 │   │
│  │  - Multi-turn Conversations                           │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐   │
│  │                  MCP Tools Layer                      │   │
│  │  - Todo CRUD Tools                                    │   │
│  │  - Query & Filter Tools                               │   │
│  │  - Batch Operations Tools                             │   │
│  │  - Context Retrieval Tools                            │   │
│  └────────────────┬─────────────────────────────────────┘   │
└───────────────────┼─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server                                │
│  - Tool Definitions                                          │
│  - Schema Validation                                         │
│  - API Client Wrapper                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 Phase II Backend API                         │
│  - Todo CRUD Endpoints                                       │
│  - User Management                                           │
│  - Database (PostgreSQL/MongoDB)                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Component Specifications

#### 2.1 Conversational Agent (OpenAI Agents SDK)

**Purpose**: Orchestrate the conversation, interpret user intent, and coordinate tool usage.

**Key Responsibilities**:
- Parse natural language input to identify user intent
- Manage conversation context and history
- Determine which tools to call and in what order
- Handle multi-turn conversations for clarification
- Format responses in a user-friendly manner

**Configuration**:
```typescript
// Agent Configuration
{
  model: "gpt-4-turbo", // or latest available model
  temperature: 0.7,
  systemPrompt: `You are a helpful task management assistant. You help users manage their todo lists through natural conversation...`,
  tools: [
    // MCP-defined tools (see section 2.2)
  ],
  maxTurns: 10,
  contextWindow: 8000
}
```

**Core Capabilities**:
1. **Intent Classification**: Identify operation types (create, read, update, delete, query)
2. **Entity Extraction**: Extract task details (title, description, priority, due date, tags)
3. **Temporal Reasoning**: Interpret relative dates ("tomorrow", "next Monday", "in 3 days")
4. **Confirmation Handling**: Recognize affirmative/negative responses
5. **Error Recovery**: Handle API failures gracefully and suggest alternatives

#### 2.2 MCP Tools Layer

**Purpose**: Define standardized tools that the agent can call to interact with the Todo backend.

**Tool Categories**:

##### A. Task Creation Tools

**Tool: `create_task`**
```json
{
  "name": "create_task",
  "description": "Create a new todo task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Task title (required)"
      },
      "description": {
        "type": "string",
        "description": "Detailed task description"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "urgent"],
        "description": "Task priority level"
      },
      "dueDate": {
        "type": "string",
        "format": "date-time",
        "description": "ISO 8601 formatted due date"
      },
      "tags": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Task tags/categories"
      },
      "metadata": {
        "type": "object",
        "description": "Additional task metadata (time, location, etc.)"
      }
    },
    "required": ["title"]
  }
}
```

##### B. Task Query Tools

**Tool: `list_tasks`**
```json
{
  "name": "list_tasks",
  "description": "Retrieve tasks based on filters",
  "inputSchema": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "enum": ["pending", "in_progress", "completed", "archived"],
        "description": "Filter by task status"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "urgent"],
        "description": "Filter by priority"
      },
      "dueDateStart": {
        "type": "string",
        "format": "date-time",
        "description": "Tasks due after this date"
      },
      "dueDateEnd": {
        "type": "string",
        "format": "date-time",
        "description": "Tasks due before this date"
      },
      "tags": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Filter by tags (OR logic)"
      },
      "searchQuery": {
        "type": "string",
        "description": "Full-text search in title/description"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results"
      }
    }
  }
}
```

**Tool: `get_task_by_id`**
```json
{
  "name": "get_task_by_id",
  "description": "Retrieve a specific task by ID",
  "inputSchema": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "string",
        "description": "Unique task identifier"
      }
    },
    "required": ["taskId"]
  }
}
```

##### C. Task Update Tools

**Tool: `update_task`**
```json
{
  "name": "update_task",
  "description": "Update one or more fields of an existing task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "string",
        "description": "Unique task identifier"
      },
      "updates": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "description": {"type": "string"},
          "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "urgent"]
          },
          "status": {
            "type": "string",
            "enum": ["pending", "in_progress", "completed", "archived"]
          },
          "dueDate": {
            "type": "string",
            "format": "date-time"
          },
          "tags": {
            "type": "array",
            "items": {"type": "string"}
          },
          "metadata": {"type": "object"}
        }
      }
    },
    "required": ["taskId", "updates"]
  }
}
```

**Tool: `mark_task_completed`**
```json
{
  "name": "mark_task_completed",
  "description": "Mark a task as completed",
  "inputSchema": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "string",
        "description": "Unique task identifier"
      }
    },
    "required": ["taskId"]
  }
}
```

##### D. Task Deletion Tools

**Tool: `delete_task`**
```json
{
  "name": "delete_task",
  "description": "Permanently delete a task",
  "inputSchema": {
    "type": "object",
    "properties": {
      "taskId": {
        "type": "string",
        "description": "Unique task identifier"
      }
    },
    "required": ["taskId"]
  }
}
```

##### E. Batch Operations Tools

**Tool: `bulk_update_tasks`**
```json
{
  "name": "bulk_update_tasks",
  "description": "Update multiple tasks at once",
  "inputSchema": {
    "type": "object",
    "properties": {
      "taskIds": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Array of task IDs to update"
      },
      "updates": {
        "type": "object",
        "description": "Updates to apply to all specified tasks"
      }
    },
    "required": ["taskIds", "updates"]
  }
}
```

**Tool: `archive_completed_tasks`**
```json
{
  "name": "archive_completed_tasks",
  "description": "Archive all completed tasks within a date range",
  "inputSchema": {
    "type": "object",
    "properties": {
      "completedBefore": {
        "type": "string",
        "format": "date-time",
        "description": "Archive tasks completed before this date"
      }
    }
  }
}
```

##### F. Context & Analytics Tools

**Tool: `get_task_summary`**
```json
{
  "name": "get_task_summary",
  "description": "Get a summary of tasks by status and priority",
  "inputSchema": {
    "type": "object",
    "properties": {
      "dateRange": {
        "type": "object",
        "properties": {
          "start": {"type": "string", "format": "date-time"},
          "end": {"type": "string", "format": "date-time"}
        }
      }
    }
  }
}
```

#### 2.3 MCP Server Implementation

**Purpose**: Host the MCP tools and translate tool calls into backend API requests.

**Technology Stack**:
- **Framework**: Official MCP SDK (TypeScript/Python)
- **HTTP Client**: Axios or Fetch API
- **Authentication**: JWT token management
- **Error Handling**: Standardized error responses

**Implementation Structure**:

```typescript
// mcp-server/src/index.ts
import { MCPServer } from '@modelcontextprotocol/sdk';
import { TodoAPIClient } from './clients/todo-api';

const server = new MCPServer({
  name: 'todo-mcp-server',
  version: '1.0.0'
});

// Initialize API client
const todoAPI = new TodoAPIClient({
  baseURL: process.env.TODO_API_URL || 'http://localhost:3000',
  apiKey: process.env.TODO_API_KEY
});

// Register tools
server.tool('create_task', createTaskHandler(todoAPI));
server.tool('list_tasks', listTasksHandler(todoAPI));
server.tool('update_task', updateTaskHandler(todoAPI));
// ... register all tools

server.start();
```

**Tool Handler Pattern**:

```typescript
// mcp-server/src/handlers/create-task.ts
export function createTaskHandler(apiClient: TodoAPIClient) {
  return async (params: CreateTaskParams) => {
    try {
      // Validate input
      const validatedParams = validateCreateTaskParams(params);

      // Call backend API
      const task = await apiClient.createTask(validatedParams);

      // Return formatted response
      return {
        success: true,
        data: task,
        message: `Task created: "${task.title}" (ID: ${task.id})`
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        code: error.code
      };
    }
  };
}
```

**Error Handling Strategy**:

```typescript
// Standardized error responses
enum ErrorCode {
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  NOT_FOUND = 'NOT_FOUND',
  UNAUTHORIZED = 'UNAUTHORIZED',
  API_ERROR = 'API_ERROR',
  NETWORK_ERROR = 'NETWORK_ERROR'
}

interface ToolResponse {
  success: boolean;
  data?: any;
  error?: string;
  code?: ErrorCode;
  message?: string;
}
```

#### 2.4 Intent Recognition & Mapping

**Intent Categories**:

| Intent | Example Phrases | Primary Tool(s) |
|--------|----------------|-----------------|
| `CREATE_TASK` | "Add a task...", "Create a todo...", "Remind me to..." | `create_task` |
| `LIST_TASKS` | "Show me...", "What are my...", "List all..." | `list_tasks` |
| `UPDATE_TASK` | "Change...", "Update...", "Modify..." | `update_task` |
| `COMPLETE_TASK` | "Mark as done...", "Complete...", "Finish..." | `mark_task_completed` |
| `DELETE_TASK` | "Delete...", "Remove...", "Cancel..." | `delete_task` |
| `RESCHEDULE_TASK` | "Reschedule...", "Move to...", "Change the date..." | `update_task` |
| `FILTER_TASKS` | "High priority tasks...", "Tasks due today..." | `list_tasks` |
| `BULK_ARCHIVE` | "Archive completed tasks...", "Clean up old tasks..." | `archive_completed_tasks` |
| `GET_SUMMARY` | "What's on my plate?", "Overview of tasks..." | `get_task_summary` |

**Temporal Expression Handling**:

The agent must interpret relative time expressions and convert them to absolute ISO 8601 timestamps:

```typescript
// Temporal expression mappings
const TEMPORAL_PATTERNS = {
  'today': () => new Date().toISOString(),
  'tomorrow': () => addDays(new Date(), 1).toISOString(),
  'next week': () => addDays(new Date(), 7).toISOString(),
  'next monday': () => nextWeekday(new Date(), 1).toISOString(),
  'in 3 days': () => addDays(new Date(), 3).toISOString(),
  'at 11 AM': (date) => setTime(date, 11, 0).toISOString()
};
```

**Ambiguity Resolution**:

When the user's intent is ambiguous, the agent should:
1. Identify the ambiguity
2. Ask a clarifying question
3. Wait for user response
4. Proceed with the clarified intent

Example:
```
User: "Reschedule my morning meetings to 2 PM"
Agent: "I found 3 tasks with 'meeting' in the title scheduled for this morning:
       1. Team standup (9 AM)
       2. Client call (10 AM)
       3. Design review (11 AM)
       Would you like to reschedule all of them to 2 PM, or specific ones?"
```

### 3. Conversation Flow Examples

#### 3.1 Simple Task Creation

```
User: Add a task to call the dentist tomorrow at 11 AM.

Agent: [Calls create_task with:
  - title: "Call the dentist"
  - dueDate: "2025-12-28T11:00:00Z"
  - metadata: { timeSpecified: true }
]

Agent: ✓ I've added "Call the dentist" to your list for tomorrow at 11 AM.
```

#### 3.2 Filtered Task Retrieval

```
User: Show me my high priority tasks for today.

Agent: [Calls list_tasks with:
  - priority: "high"
  - dueDateStart: "2025-12-27T00:00:00Z"
  - dueDateEnd: "2025-12-27T23:59:59Z"
]

Agent: You have 2 high priority tasks for today:
       1. Finish quarterly report (due 5 PM)
       2. Review pull request #423 (due end of day)
```

#### 3.3 Bulk Archive with Confirmation

```
User: Mark all completed tasks from yesterday as archived.

Agent: [Calls list_tasks to find completed tasks from yesterday]

Agent: I found 5 completed tasks from yesterday:
       1. Review design mockups
       2. Send invoice to client
       3. Update dependencies
       4. Team check-in
       5. Code review

       Would you like me to archive all of these?

User: Yes

Agent: [Calls archive_completed_tasks with completedBefore: "2025-12-27T00:00:00Z"]

Agent: ✓ Archived 5 tasks from yesterday.
```

#### 3.4 Reschedule with Disambiguation

```
User: Reschedule my morning meetings to 2 PM.

Agent: [Calls list_tasks to find tasks with "meeting" due this morning]

Agent: I found 2 tasks that might be meetings scheduled for this morning:
       1. "Team standup" at 9 AM
       2. "1:1 with Sarah" at 10:30 AM

       Should I reschedule both to 2 PM, or just one?

User: Both

Agent: [Calls bulk_update_tasks with:
  - taskIds: ["task-123", "task-456"]
  - updates: { dueDate: "2025-12-27T14:00:00Z" }
]

Agent: ✓ Rescheduled both meetings to 2 PM today:
       - Team standup
       - 1:1 with Sarah
```

#### 3.5 Complex Query

```
User: What tasks do I have this week that are urgent or related to the launch?

Agent: [Calls list_tasks with:
  - dueDateStart: "2025-12-27T00:00:00Z"
  - dueDateEnd: "2026-01-03T23:59:59Z"
  - Complex filter: priority=urgent OR tags contains "launch"
]

Agent: You have 4 tasks matching your criteria:

       Urgent:
       1. Fix critical bug in checkout flow (due today)
       2. Approve marketing copy (due Dec 28)

       Launch-related:
       3. Final QA testing [launch] (due Dec 30)
       4. Prepare launch announcement [launch] (due Jan 2)
```

#### 3.6 Task Update

```
User: Change the priority of "Finish quarterly report" to urgent.

Agent: [Calls list_tasks with searchQuery: "Finish quarterly report"]

Agent: [Calls update_task with:
  - taskId: "task-789"
  - updates: { priority: "urgent" }
]

Agent: ✓ Updated "Finish quarterly report" to urgent priority.
```

#### 3.7 Error Handling

```
User: Delete my task about the dentist.

Agent: [Calls list_tasks with searchQuery: "dentist"]

Agent: I found 2 tasks mentioning "dentist":
       1. Call the dentist (due tomorrow)
       2. Dentist appointment (due next week)

       Which one would you like to delete?

User: The first one

Agent: [Calls delete_task with taskId: "task-101"]
       [API returns 404 - task not found]

Agent: I'm sorry, but I couldn't delete that task. It appears to have been
       already deleted or doesn't exist anymore. Would you like me to show
       you your current tasks?
```

#### 3.8 Summary Request

```
User: What's on my plate today?

Agent: [Calls get_task_summary with today's date range]
       [Calls list_tasks for today's tasks]

Agent: Here's your overview for today:

       📊 Summary:
       - 3 pending tasks
       - 1 in progress
       - 2 completed

       🔥 High Priority:
       1. Finish quarterly report (due 5 PM)
       2. Review pull request #423 (due EOD)

       📝 Other Tasks:
       3. Team standup (9 AM) - completed
       4. Update project timeline (due 6 PM)
       5. Prepare presentation slides (no deadline)
```

### 4. System Prompts & Agent Configuration

#### 4.1 Main System Prompt

```
You are TodoBot, an intelligent task management assistant. You help users
manage their todo lists through natural conversation.

Your capabilities:
- Create, read, update, and delete tasks
- Filter and search tasks by various criteria
- Handle relative dates (today, tomorrow, next week, etc.)
- Perform bulk operations with user confirmation
- Provide task summaries and overviews

Guidelines:
1. Always confirm before performing destructive operations (delete, bulk archive)
2. When ambiguous, ask clarifying questions rather than guessing
3. Use clear, concise language
4. Format lists and summaries for readability
5. Acknowledge successful operations explicitly
6. If an operation fails, explain why and suggest alternatives
7. Interpret relative time expressions accurately
8. When multiple tasks match a description, list them and ask for clarification

Task Priority Levels:
- low: Nice to have, no urgency
- medium: Standard tasks, should be completed reasonably soon
- high: Important tasks requiring attention
- urgent: Critical tasks requiring immediate action

Task Statuses:
- pending: Not yet started
- in_progress: Currently being worked on
- completed: Finished but not archived
- archived: Completed and archived for history

Always use the available tools to interact with the todo system. Never
make up task information or IDs.
```

#### 4.2 Tool Usage Guidelines Prompt

```
When using tools:

1. For CREATE operations:
   - Extract all relevant details from user input
   - Convert relative dates to ISO 8601 format
   - Default priority to "medium" if not specified
   - Default status to "pending" for new tasks

2. For QUERY operations:
   - Use specific filters rather than retrieving all tasks
   - Limit results to reasonable numbers (10-20 for lists)
   - Use searchQuery for text-based searches

3. For UPDATE operations:
   - First search for the task if only a description is given
   - If multiple matches, ask user to clarify
   - Only update specified fields, keep others unchanged

4. For DELETE operations:
   - Always confirm before deleting
   - Show task details before deletion
   - Handle "delete all" requests with extreme caution

5. For BULK operations:
   - List affected tasks before acting
   - Require explicit confirmation
   - Report results clearly (X tasks affected)
```

### 5. Integration Architecture

#### 5.1 Authentication Flow

```
┌──────┐                           ┌─────────────┐                    ┌──────────┐
│ User │                           │ MCP Server  │                    │ Backend  │
└───┬──┘                           └──────┬──────┘                    └────┬─────┘
    │                                     │                                │
    │ 1. Start conversation               │                                │
    ├────────────────────────────────────>│                                │
    │                                     │                                │
    │                                     │ 2. Authenticate                │
    │                                     ├───────────────────────────────>│
    │                                     │                                │
    │                                     │ 3. Return JWT token            │
    │                                     │<───────────────────────────────┤
    │                                     │                                │
    │ 4. User request (via agent)         │                                │
    ├────────────────────────────────────>│                                │
    │                                     │                                │
    │                                     │ 5. API call (with JWT)         │
    │                                     ├───────────────────────────────>│
    │                                     │                                │
    │                                     │ 6. Response                    │
    │                                     │<───────────────────────────────┤
    │                                     │                                │
    │ 7. Formatted response               │                                │
    │<────────────────────────────────────┤                                │
```

**Configuration**:
```typescript
// .env configuration
TODO_API_URL=http://localhost:3000
TODO_API_KEY=your-api-key-here
OPENAI_API_KEY=your-openai-key-here
MCP_SERVER_PORT=3001
```

#### 5.2 Data Flow for a Typical Request

```
User Input: "Add a task to call the dentist tomorrow at 11 AM"
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ OpenAI Agent (Intent Recognition)                       │
│ - Intent: CREATE_TASK                                   │
│ - Entities:                                             │
│   * title: "Call the dentist"                           │
│   * dueDate: "tomorrow at 11 AM"                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Agent Decision: Use create_task tool                     │
│ - Convert "tomorrow at 11 AM" to ISO 8601               │
│ - Result: "2025-12-28T11:00:00Z"                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ MCP Tool Call: create_task                              │
│ {                                                        │
│   title: "Call the dentist",                            │
│   dueDate: "2025-12-28T11:00:00Z",                      │
│   metadata: { timeSpecified: true }                     │
│ }                                                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ MCP Server Handler                                       │
│ - Validate input schema                                 │
│ - Call TodoAPIClient.createTask()                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ HTTP Request to Backend API                             │
│ POST /api/tasks                                         │
│ Headers: { Authorization: "Bearer <JWT>" }              │
│ Body: { title, dueDate, metadata }                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Backend Response                                         │
│ {                                                        │
│   id: "task-12345",                                     │
│   title: "Call the dentist",                            │
│   dueDate: "2025-12-28T11:00:00Z",                      │
│   status: "pending",                                    │
│   createdAt: "2025-12-27T10:30:00Z"                     │
│ }                                                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ MCP Server Response                                      │
│ {                                                        │
│   success: true,                                        │
│   data: { ... task object ... },                        │
│   message: "Task created: ..."                          │
│ }                                                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Agent Response Generation                               │
│ "✓ I've added 'Call the dentist' to your list for      │
│  tomorrow at 11 AM."                                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
                    User receives response
```

#### 5.3 Context Management

**Conversation History**:
- Maintain last N turns of conversation for context
- Store task IDs mentioned in recent conversation
- Track pending confirmations

```typescript
interface ConversationContext {
  userId: string;
  conversationId: string;
  history: Message[];
  recentTasks: string[]; // Task IDs mentioned recently
  pendingConfirmation?: {
    action: string;
    taskIds: string[];
    confirmationPrompt: string;
  };
  preferences: UserPreferences;
}
```

**Task Context Retrieval**:
- Before responding, agent can call `get_task_summary` to understand user's current workload
- Use this context to provide proactive suggestions

Example:
```
User: What should I focus on today?

Agent: [Calls get_task_summary for today]
       [Analyzes priorities and deadlines]

Agent: Based on your tasks, I recommend focusing on these high-priority items:
       1. Finish quarterly report (due 5 PM) - URGENT
       2. Review pull request #423 (due EOD)

       You also have 3 lower-priority tasks that can wait if needed.
```

### 6. Error Handling & Edge Cases

#### 6.1 Backend API Errors

| Error Type | HTTP Status | MCP Response | Agent Behavior |
|------------|-------------|--------------|----------------|
| Invalid input | 400 | `{success: false, code: 'VALIDATION_ERROR'}` | Inform user, suggest correction |
| Unauthorized | 401 | `{success: false, code: 'UNAUTHORIZED'}` | Inform user to re-authenticate |
| Not found | 404 | `{success: false, code: 'NOT_FOUND'}` | Inform user item doesn't exist |
| Server error | 500 | `{success: false, code: 'API_ERROR'}` | Apologize, suggest retry |
| Network error | - | `{success: false, code: 'NETWORK_ERROR'}` | Inform user, suggest check connection |

#### 6.2 Ambiguous Queries

**Strategy**: Ask clarifying questions rather than guessing.

Examples:
```
User: "Delete my meeting"
→ Multiple meetings found → List and ask which one

User: "Show me tasks for next week"
→ Unclear if Mon-Sun or 7 days from now → Ask for clarification or use sensible default (Mon-Sun)

User: "Make it high priority"
→ No recent task context → Ask which task
```

#### 6.3 Impossible Requests

```
User: "Show me tasks I'll complete next year"

Agent: I can show you tasks scheduled for next year, but I can't predict
       which ones you'll actually complete. Would you like to see tasks
       scheduled for next year instead?
```

#### 6.4 Rate Limiting & Performance

- MCP server should implement request queuing for bulk operations
- Agent should batch multiple updates when possible
- Inform user if operation will take time: "Processing 50 tasks, this may take a moment..."

### 7. Deployment Configuration

#### 7.1 Local Development Setup

**Prerequisites**:
- Node.js 18+
- Phase II backend running on `localhost:3000`
- OpenAI API key
- MCP SDK installed

**Directory Structure**:
```
phase-iii-chatbot/
├── mcp-server/
│   ├── src/
│   │   ├── index.ts              # MCP server entry point
│   │   ├── tools/                # Tool definitions
│   │   │   ├── create-task.ts
│   │   │   ├── list-tasks.ts
│   │   │   ├── update-task.ts
│   │   │   └── ...
│   │   ├── clients/
│   │   │   └── todo-api.ts       # Backend API client
│   │   ├── utils/
│   │   │   ├── date-parser.ts    # Temporal expression parsing
│   │   │   └── validators.ts     # Input validation
│   │   └── types/
│   │       └── index.ts          # TypeScript types
│   ├── package.json
│   └── tsconfig.json
├── agent/
│   ├── src/
│   │   ├── index.ts              # Agent setup
│   │   ├── prompts/
│   │   │   ├── system.ts         # System prompts
│   │   │   └── guidelines.ts     # Tool usage guidelines
│   │   └── context/
│   │       └── manager.ts        # Conversation context
│   ├── package.json
│   └── tsconfig.json
├── cli-client/                    # Simple CLI for testing
│   └── index.ts
├── .env.example
└── README.md
```

**Installation Steps**:
```bash
# 1. Install dependencies
cd phase-iii-chatbot/mcp-server
npm install

cd ../agent
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys and URLs

# 3. Start MCP server
cd mcp-server
npm run dev

# 4. In another terminal, start agent
cd agent
npm run dev

# 5. Test with CLI client
cd cli-client
npm start
```

#### 7.2 Environment Variables

```bash
# .env.example

# Backend API
TODO_API_URL=http://localhost:3000
TODO_API_KEY=your-backend-api-key

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-turbo

# MCP Server
MCP_SERVER_PORT=3001
MCP_SERVER_HOST=localhost

# Agent Configuration
AGENT_MAX_TURNS=10
AGENT_TEMPERATURE=0.7
AGENT_CONTEXT_WINDOW=8000

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

### 8. Testing Strategy

#### 8.1 Unit Tests

**MCP Tool Handlers**:
```typescript
describe('create_task handler', () => {
  it('should create a task with valid input', async () => {
    const handler = createTaskHandler(mockAPIClient);
    const result = await handler({
      title: 'Test task',
      priority: 'high'
    });

    expect(result.success).toBe(true);
    expect(result.data.title).toBe('Test task');
  });

  it('should return validation error for missing title', async () => {
    const handler = createTaskHandler(mockAPIClient);
    const result = await handler({ description: 'No title' });

    expect(result.success).toBe(false);
    expect(result.code).toBe('VALIDATION_ERROR');
  });
});
```

**Date Parser**:
```typescript
describe('parseTemporalExpression', () => {
  it('should parse "tomorrow" correctly', () => {
    const result = parseTemporalExpression('tomorrow');
    const expected = addDays(new Date(), 1);
    expect(isSameDay(result, expected)).toBe(true);
  });

  it('should parse "next Monday at 2 PM" correctly', () => {
    const result = parseTemporalExpression('next Monday at 2 PM');
    expect(result.getHours()).toBe(14);
    expect(result.getDay()).toBe(1); // Monday
  });
});
```

#### 8.2 Integration Tests

**MCP Server → Backend API**:
```typescript
describe('MCP Server Integration', () => {
  it('should successfully create task via backend API', async () => {
    const response = await mcpClient.callTool('create_task', {
      title: 'Integration test task'
    });

    expect(response.success).toBe(true);

    // Verify in backend
    const task = await backendAPI.getTask(response.data.id);
    expect(task.title).toBe('Integration test task');
  });
});
```

#### 8.3 End-to-End Conversation Tests

**Scripted Conversations**:
```typescript
describe('Chatbot E2E Tests', () => {
  it('should handle task creation conversation', async () => {
    const conversation = new TestConversation();

    const response1 = await conversation.send(
      "Add a task to call the dentist tomorrow at 11 AM"
    );
    expect(response1).toContain("I've added");
    expect(response1).toContain("Call the dentist");
    expect(response1).toContain("tomorrow at 11 AM");

    // Verify task was created
    const tasks = await conversation.send("Show me tomorrow's tasks");
    expect(tasks).toContain("Call the dentist");
  });

  it('should handle bulk archive with confirmation', async () => {
    const conversation = new TestConversation();

    // Setup: create completed tasks
    await createCompletedTasks(5, 'yesterday');

    const response1 = await conversation.send(
      "Archive all completed tasks from yesterday"
    );
    expect(response1).toContain("I found 5 completed tasks");
    expect(response1).toContain("archive all");

    const response2 = await conversation.send("Yes");
    expect(response2).toContain("Archived 5 tasks");
  });
});
```

### 9. Acceptance Criteria

Phase III is considered complete when the chatbot successfully handles all of the following scripted conversations:

#### 9.1 Core CRUD Operations

✅ **AC-1: Create simple task**
```
User: "Add a task to buy groceries"
Expected: Task created with title "buy groceries", default priority, no due date
```

✅ **AC-2: Create task with details**
```
User: "Add a high priority task to submit expense report by Friday 5 PM"
Expected: Task created with priority=high, due date=next Friday 5 PM
```

✅ **AC-3: List all tasks**
```
User: "Show me all my tasks"
Expected: Returns list of all pending/in-progress tasks
```

✅ **AC-4: List filtered tasks**
```
User: "Show me high priority tasks due today"
Expected: Returns only high priority tasks with today's due date
```

✅ **AC-5: Update task priority**
```
User: "Change the priority of 'submit expense report' to urgent"
Expected: Task priority updated to urgent
```

✅ **AC-6: Mark task complete**
```
User: "Mark 'buy groceries' as done"
Expected: Task status changed to completed
```

✅ **AC-7: Delete task**
```
User: "Delete the task about groceries"
Expected: After confirmation, task is deleted
```

#### 9.2 Complex Queries

✅ **AC-8: Date range query**
```
User: "What tasks do I have this week?"
Expected: Returns tasks with due dates in current week (Mon-Sun)
```

✅ **AC-9: Multi-criteria filter**
```
User: "Show me urgent tasks related to the launch"
Expected: Returns tasks with priority=urgent OR tags containing "launch"
```

✅ **AC-10: Search query**
```
User: "Find tasks mentioning 'dentist'"
Expected: Returns tasks with "dentist" in title or description
```

#### 9.3 Bulk Operations

✅ **AC-11: Bulk update with confirmation**
```
User: "Reschedule all my morning meetings to 2 PM"
Agent: "I found 3 meetings... Should I reschedule all?"
User: "Yes"
Expected: All identified tasks updated to 2 PM
```

✅ **AC-12: Bulk archive**
```
User: "Archive all completed tasks from last week"
Agent: "I found 8 completed tasks... Archive all?"
User: "Yes"
Expected: 8 tasks archived
```

#### 9.4 Temporal Reasoning

✅ **AC-13: Relative date - tomorrow**
```
User: "Remind me to call John tomorrow"
Expected: Task created with due date = tomorrow (no time specified)
```

✅ **AC-14: Relative date - specific time**
```
User: "Schedule meeting review for next Monday at 3 PM"
Expected: Task created with due date = next Monday at 3 PM
```

✅ **AC-15: Relative date - days from now**
```
User: "Add task to review code in 3 days"
Expected: Task created with due date = 3 days from now
```

#### 9.5 Error Handling & Disambiguation

✅ **AC-16: Ambiguous task reference**
```
User: "Delete my meeting"
Agent: "I found 2 tasks with 'meeting'... Which one?"
User: "The first one"
Expected: Correct task deleted
```

✅ **AC-17: Not found error**
```
User: "Show me the task about XYZ"
Agent: "I couldn't find any tasks matching 'XYZ'"
Expected: Graceful error message
```

✅ **AC-18: API error handling**
```
Scenario: Backend API is down
User: "Add a task to test something"
Expected: Agent informs user of connection issue, suggests retry
```

#### 9.6 Context & Summaries

✅ **AC-19: Task summary**
```
User: "What's on my plate today?"
Expected: Summary showing count by status, high priority tasks listed
```

✅ **AC-20: Proactive context use**
```
User: "What should I focus on?"
Expected: Agent analyzes tasks and recommends prioritization
```

### 10. Success Metrics

**Phase III is successful when**:

1. **Functional Completeness**: All 20 acceptance criteria pass
2. **Response Quality**:
   - 95%+ of user intents correctly identified
   - Zero hallucinated task data
   - Clear, concise responses (avg < 50 words for simple operations)
3. **Performance**:
   - Average response time < 3 seconds for simple operations
   - Bulk operations complete within 10 seconds for up to 50 tasks
4. **Reliability**:
   - 99%+ uptime for MCP server
   - Graceful degradation when backend is unavailable
   - No data loss or corruption

### 11. Future Enhancements (Phase IV+)

Items explicitly out of scope for Phase III but planned for future phases:

- Multi-user conversations and task delegation
- Voice interface integration
- Recurring task patterns
- Natural language reminders/notifications
- Smart suggestions based on task history
- Integration with external calendars (Google Calendar, Outlook)
- Mobile app interface
- Kubernetes deployment
- Event-driven architecture with Kafka
- Analytics and productivity insights

---

## Appendix

### A. Sample MCP Tool Definition (JSON Schema)

```json
{
  "name": "create_task",
  "description": "Create a new todo task with optional metadata",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Task title (required)",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "type": "string",
        "description": "Detailed task description",
        "maxLength": 2000
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high", "urgent"],
        "description": "Task priority level",
        "default": "medium"
      },
      "status": {
        "type": "string",
        "enum": ["pending", "in_progress", "completed", "archived"],
        "description": "Task status",
        "default": "pending"
      },
      "dueDate": {
        "type": "string",
        "format": "date-time",
        "description": "ISO 8601 formatted due date"
      },
      "tags": {
        "type": "array",
        "items": {
          "type": "string",
          "maxLength": 50
        },
        "description": "Task tags/categories",
        "maxItems": 10
      },
      "metadata": {
        "type": "object",
        "description": "Additional task metadata",
        "properties": {
          "timeSpecified": {
            "type": "boolean",
            "description": "Whether a specific time was mentioned"
          },
          "location": {
            "type": "string",
            "description": "Task location if specified"
          },
          "estimatedDuration": {
            "type": "number",
            "description": "Estimated duration in minutes"
          }
        }
      }
    },
    "required": ["title"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "success": {
        "type": "boolean"
      },
      "data": {
        "type": "object",
        "description": "Created task object"
      },
      "message": {
        "type": "string"
      },
      "error": {
        "type": "string"
      },
      "code": {
        "type": "string",
        "enum": [
          "VALIDATION_ERROR",
          "NOT_FOUND",
          "UNAUTHORIZED",
          "API_ERROR",
          "NETWORK_ERROR"
        ]
      }
    }
  }
}
```

### B. Temporal Expression Grammar

```
temporal_expression := relative_day [time_expression]
                     | specific_weekday [time_expression]
                     | date_offset [time_expression]

relative_day := "today" | "tomorrow" | "yesterday"

specific_weekday := ["next" | "this"] weekday
weekday := "monday" | "tuesday" | "wednesday" | "thursday" | "friday" | "saturday" | "sunday"

date_offset := "in" number ("day" | "days" | "week" | "weeks" | "month" | "months")

time_expression := "at" time
time := hour [":" minutes] [am_pm]
hour := number (1-12 with am_pm, 0-23 without)
minutes := number (0-59)
am_pm := "AM" | "PM" | "am" | "pm"
```

### C. Backend API Endpoints Reference

The MCP server will interact with these Phase II backend endpoints:

```
POST   /api/tasks              - Create new task
GET    /api/tasks              - List tasks (with query params)
GET    /api/tasks/:id          - Get specific task
PUT    /api/tasks/:id          - Update task
DELETE /api/tasks/:id          - Delete task
PATCH  /api/tasks/bulk-update  - Bulk update tasks
POST   /api/tasks/archive      - Archive tasks by criteria
GET    /api/tasks/summary      - Get task statistics
```

### D. Development Checklist

**MCP Server**:
- [ ] Set up MCP SDK project structure
- [ ] Implement TodoAPIClient wrapper
- [ ] Define all tool schemas
- [ ] Implement tool handlers (create, read, update, delete)
- [ ] Implement bulk operation handlers
- [ ] Add input validation
- [ ] Add error handling and logging
- [ ] Write unit tests for handlers
- [ ] Write integration tests with backend

**Agent**:
- [ ] Set up OpenAI Agents SDK
- [ ] Configure system prompts
- [ ] Implement temporal expression parser
- [ ] Implement conversation context manager
- [ ] Configure tool usage guidelines
- [ ] Add confirmation flow logic
- [ ] Write E2E conversation tests
- [ ] Test all 20 acceptance criteria

**CLI Client**:
- [ ] Create simple readline-based CLI
- [ ] Implement conversation display formatting
- [ ] Add session management
- [ ] Add command history

**Documentation**:
- [ ] Write setup/installation guide
- [ ] Document environment configuration
- [ ] Create troubleshooting guide
- [ ] Document testing procedures

---

## Document Metadata

- **Version**: 1.0.0
- **Created**: 2025-12-27
- **Last Updated**: 2025-12-27
- **Status**: Draft for Review
- **Authors**: Evolution of Todo Project Team
- **Phase**: III - AI-Powered Chatbot
- **Dependencies**: Phase II Backend (Complete)

---

## Approval & Sign-off

This specification requires approval before implementation begins:

- [ ] Technical Lead Review
- [ ] Architecture Review
- [ ] Product Owner Approval
- [ ] Security Review (if applicable)

**Next Steps After Approval**:
1. Create detailed implementation plan
2. Set up project repositories
3. Begin MCP server development
4. Parallel development of agent configuration
5. Iterative testing against acceptance criteria
