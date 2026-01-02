# DBeaver PostgreSQL Connection Guide

## Connection Details for Your testdb

### Method 1: Using DBeaver UI
```
1. Open DBeaver
2. Click "New Database Connection" (plug icon) or Database -> New Database Connection
3. Select "PostgreSQL" 
4. Click "Next"

5. Fill in Connection Settings:
   ┌─────────────────────────────────────┐
   │ Host:         localhost             │
   │ Port:         5432                  │
   │ Database:     testdb                │
   │ Username:     todo_user             │
   │ Password:     todo_pass             │
   │ Show all databases: ☐ (unchecked)  │
   └─────────────────────────────────────┘

6. Click "Test Connection"
   - If asked to download drivers, click "Download"
   
7. Click "Finish"
```

### Method 2: Using Connection URL
```
URL: jdbc:postgresql://localhost:5432/testdb
Username: todo_user
Password: todo_pass
```

## After Connection

You will see:
```
testdb
├── Schemas
│   └── public
│       ├── Tables
│       │   ├── tasks (7 rows)
│       │   ├── users (1 row)
│       │   ├── tags (4 rows)
│       │   └── task_tags
│       ├── Views
│       └── ...
```

## Quick SQL Queries to Run

```sql
-- View all tasks
SELECT * FROM tasks ORDER BY created_at DESC;

-- Count tasks by priority
SELECT priority, COUNT(*) FROM tasks GROUP BY priority;

-- View tasks with tags
SELECT t.id, t.title, t.priority, 
       array_agg(tg.name) as tags
FROM tasks t
LEFT JOIN task_tags tt ON t.id = tt.task_id
LEFT JOIN tags tg ON tt.tag_id = tg.id
GROUP BY t.id, t.title, t.priority;
```

## Troubleshooting

**Error: "Connection refused"**
- Make sure Docker containers are running: `docker ps`
- Port 5432 should be accessible: `docker ps | grep 5432`

**Error: "Authentication failed"**
- Double-check username: `todo_user`
- Double-check password: `todo_pass`
- Database name: `testdb`
