# Docker Setup Guide

This guide explains how to run the Todo application using Docker and Docker Compose.

## Prerequisites

- Docker Desktop installed (includes Docker Compose)
- Docker running on your system

## Understanding the Architecture

When running with Docker:

```
┌─────────────────────────────────────────────────┐
│ Host Machine (Your Computer)                    │
│                                                  │
│  Browser ──> localhost:3000 (Frontend)          │
│         └──> localhost:8000 (Backend)           │
│                                                  │
│  ┌───────────────────────────────────────────┐ │
│  │ Docker Network                            │ │
│  │                                           │ │
│  │  Frontend Container                       │ │
│  │  ├─ Server-side: calls backend:8000      │ │
│  │  └─ Client-side: calls localhost:8000    │ │
│  │                                           │ │
│  │  Backend Container                        │ │
│  │  └─ Accessible as "backend" internally    │ │
│  │     and "localhost:8000" from host        │ │
│  │                                           │ │
│  │  PostgreSQL Container                     │ │
│  │  └─ Accessible as "postgres" internally   │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## Quick Start

### 1. Start All Services

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2
docker-compose up --build
```

**What this does:**
- Builds Docker images for backend and frontend
- Starts PostgreSQL, Backend, and Frontend containers
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`

### 2. Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### 3. Stop Services

```bash
# Stop and remove containers
docker-compose down

# Stop, remove containers, and delete volumes (including database data)
docker-compose down -v
```

## Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Restart a Service

```bash
docker-compose restart backend
docker-compose restart frontend
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up --build

# Rebuild specific service
docker-compose up --build backend
```

### Execute Commands Inside Containers

```bash
# Backend shell
docker-compose exec backend sh

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed data
docker-compose exec backend python scripts/seed_data.py

# Frontend shell
docker-compose exec frontend sh
```

## Troubleshooting

### Issue: Frontend shows "Make sure the backend server is running"

**Cause:** The frontend container can't reach the backend.

**Solution:**
1. Check if backend is running:
   ```bash
   docker-compose ps
   ```

2. Check backend logs:
   ```bash
   docker-compose logs backend
   ```

3. Test backend directly:
   ```bash
   curl http://localhost:8000/health
   ```

4. Verify environment variables in docker-compose.yml:
   - Frontend `NEXT_PUBLIC_API_URL` should be `http://localhost:8000` (for browser)
   - Frontend `INTERNAL_API_URL` should be `http://backend:8000` (for server-side)

### Issue: Backend can't connect to PostgreSQL

**Cause:** PostgreSQL not ready or wrong connection string.

**Solution:**
1. Wait for PostgreSQL health check:
   ```bash
   docker-compose logs postgres
   ```

2. Verify DATABASE_URL in docker-compose.yml:
   ```
   DATABASE_URL: postgresql+asyncpg://todo_user:todo_pass@postgres:5432/todo_db
   ```

3. Restart services in order:
   ```bash
   docker-compose down
   docker-compose up -d postgres
   # Wait 10 seconds
   docker-compose up -d backend
   docker-compose up -d frontend
   ```

### Issue: Changes not reflecting

**Cause:** Docker cached old build or volumes.

**Solution:**
```bash
# Rebuild without cache
docker-compose build --no-cache

# Or remove everything and start fresh
docker-compose down -v
docker-compose up --build
```

### Issue: Port already in use

**Cause:** Another service using 3000, 8000, or 5432.

**Solution:**
```bash
# Find what's using the port (Linux/Mac)
lsof -i :8000
lsof -i :3000

# Find what's using the port (Windows)
netstat -ano | findstr :8000

# Kill the process or change ports in docker-compose.yml
```

## Environment Variables

### Backend (.env or docker-compose.yml)

- `DATABASE_URL`: PostgreSQL connection string
- `CORS_ORIGINS`: Allowed frontend origins
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

### Frontend (.env.local or docker-compose.yml)

- `NEXT_PUBLIC_API_URL`: Backend URL for browser (client-side)
- `INTERNAL_API_URL`: Backend URL for Next.js server (SSR)

## Development vs Production

### Current Setup (Development)

- Uses `npm run dev` for hot-reloading
- Uses `uvicorn --reload` for backend auto-restart
- Mounts source code as volumes
- Exposes all ports to host

### For Production

Modify docker-compose.yml:

```yaml
# Backend
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
command: sh -c "npm run build && npm start"
```

## File Structure

```
phase2/
├── docker-compose.yml        # Main Docker Compose configuration
├── backend/
│   ├── Dockerfile           # Backend image definition
│   ├── .dockerignore       # Files to exclude from image
│   ├── requirements.txt    # Python dependencies
│   └── app/                # Application code
└── frontend/
    ├── Dockerfile          # Frontend image definition
    ├── .dockerignore      # Files to exclude from image
    ├── package.json       # Node dependencies
    └── app/               # Next.js application
```

## Best Practices

1. **Always use docker-compose down before up**: Ensures clean state
2. **Check logs if something fails**: `docker-compose logs -f`
3. **Use --build when code changes**: `docker-compose up --build`
4. **Don't commit .env files**: They contain sensitive data
5. **Use volumes for persistence**: Database data survives container restarts

## WSL-Specific Notes

Since you're using WSL (Windows Subsystem for Linux):

1. **File Permissions**: Docker volumes from WSL may have permission issues
   ```bash
   # If you see permission errors
   chmod -R 755 backend/
   chmod -R 755 frontend/
   ```

2. **Path Issues**: Use full WSL paths in volume mounts
   - Current setup uses relative paths (`./backend:/app`) which works fine

3. **Performance**: Docker Desktop for Windows + WSL2 should be fast
   - If slow, ensure WSL2 is used (not WSL1)
   - Keep code in WSL filesystem, not Windows filesystem

4. **Docker Desktop Settings**:
   - Enable WSL2 integration for your distro
   - Resources → WSL Integration → Enable for your distribution

## Testing the Setup

After starting with `docker-compose up`, verify everything works:

```bash
# 1. Test backend health
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"1.0.0"}

# 2. Test backend API
curl http://localhost:8000/api/v1/tasks
# Expected: JSON with tasks array

# 3. Test frontend (in browser)
# Open http://localhost:3000
# Should show task list without error message

# 4. Test database
docker-compose exec postgres psql -U todo_user -d todo_db -c "\dt"
# Should show tables: users, tasks, tags, task_tags
```

## Need Help?

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review docker-compose logs: `docker-compose logs -f`
3. Ensure Docker Desktop is running
4. Try clean restart: `docker-compose down -v && docker-compose up --build`
