# Production Deployment Guide

## Overview
This guide covers deploying the Todo Application in production mode using Docker.

## Prerequisites
- Docker 20.10+
- Docker Compose v2.0+
- 2GB RAM minimum
- 10GB disk space

## Quick Start - Production

### 1. Build Production Images
```bash
# Build all services
docker compose -f docker-compose.prod.yml build

# Or build individually
docker compose -f docker-compose.prod.yml build backend
docker compose -f docker-compose.prod.yml build frontend
```

### 2. Start Production Services
```bash
# Start all services
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs -f
```

### 3. Seed Database (First Time)
```bash
docker exec todo-backend-prod python scripts/seed_data.py
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development vs Production

### Development Mode (Current)
```bash
# Start development
docker compose up -d

# Hot reload enabled
# Development dependencies included
# Debug mode ON
```

### Production Mode
```bash
# Start production
docker compose -f docker-compose.prod.yml up -d

# Optimized builds
# Multi-stage Dockerfiles
# Non-root users
# Health checks
# Debug mode OFF
```

## Configuration

### Environment Variables
Copy and customize `.env.production`:
```bash
cp .env.production .env.prod

# Edit .env.prod with your values
nano .env.prod

# Use in production
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Key Variables
```env
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=change_this_password
POSTGRES_DB=testdb
NEXT_PUBLIC_API_URL=https://your-domain.com
```

## Production Features

### Backend (FastAPI)
✅ Multi-stage Docker build
✅ Non-root user (appuser)
✅ Health checks every 30s
✅ 2 Uvicorn workers
✅ Production-only dependencies
✅ Debug mode disabled

### Frontend (Next.js)
✅ Standalone output (smaller image)
✅ Multi-stage build
✅ Static optimization
✅ Non-root user
✅ Telemetry disabled
✅ Production build

### Database (PostgreSQL)
✅ Data persistence
✅ Health checks
✅ Automatic restart
✅ Isolated network

## Database Management

### DBeaver Connection
```
Host:     localhost
Port:     5432
Database: testdb
Username: todo_user
Password: todo_pass
```

### Manual Database Access
```bash
# Access PostgreSQL shell
docker exec -it todo-postgres-prod psql -U todo_user -d testdb

# View tables
\dt

# View tasks
SELECT * FROM tasks;

# Exit
\q
```

### Backup Database
```bash
# Create backup
docker exec todo-postgres-prod pg_dump -U todo_user testdb > backup.sql

# Restore backup
cat backup.sql | docker exec -i todo-postgres-prod psql -U todo_user testdb
```

## Monitoring

### Check Health
```bash
# Backend health
curl http://localhost:8000/health

# Database health
docker exec todo-postgres-prod pg_isready -U todo_user

# All services
docker compose -f docker-compose.prod.yml ps
```

### View Logs
```bash
# All logs
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker compose -f docker-compose.prod.yml logs -f backend

# Last 100 lines
docker compose -f docker-compose.prod.yml logs --tail=100
```

## Scaling

### Increase Backend Workers
Edit `docker-compose.prod.yml`:
```yaml
backend:
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Scale Services
```bash
# Run 3 backend instances
docker compose -f docker-compose.prod.yml up -d --scale backend=3
```

## Troubleshooting

### Build Fails
```bash
# Clean build
docker compose -f docker-compose.prod.yml build --no-cache

# Remove old images
docker system prune -a
```

### Port Already in Use
```bash
# Change ports in .env.prod
FRONTEND_PORT=3001
BACKEND_PORT=8001
POSTGRES_PORT=5433
```

### Database Connection Failed
```bash
# Check database is running
docker compose -f docker-compose.prod.yml ps postgres

# View database logs
docker compose -f docker-compose.prod.yml logs postgres

# Restart database
docker compose -f docker-compose.prod.yml restart postgres
```

### Frontend Can't Reach Backend
```bash
# Check NEXT_PUBLIC_API_URL in .env.prod
# For local: http://localhost:8000
# For production: https://api.yourdomain.com

# Verify CORS settings in backend
```

## Maintenance

### Update Application
```bash
# Pull latest code
git pull

# Rebuild images
docker compose -f docker-compose.prod.yml build

# Restart with new images
docker compose -f docker-compose.prod.yml up -d
```

### Clean Up
```bash
# Stop all services
docker compose -f docker-compose.prod.yml down

# Remove volumes (⚠ deletes data)
docker compose -f docker-compose.prod.yml down -v

# Remove images
docker rmi phase2-backend phase2-frontend
```

## Security Checklist

- [ ] Change default database password
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (use reverse proxy like Nginx)
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor logs
- [ ] Use strong passwords

## Deployment to Cloud

### AWS / DigitalOcean / VPS
```bash
# 1. SSH into server
ssh user@your-server.com

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Clone repository
git clone your-repo-url
cd phase2

# 4. Configure environment
cp .env.production .env.prod
nano .env.prod

# 5. Deploy
docker compose -f docker-compose.prod.yml up -d
```

### Using Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## Performance Tips

1. **Use CDN** for static assets
2. **Enable caching** for API responses
3. **Optimize images** before uploading
4. **Monitor** resource usage
5. **Scale horizontally** when needed

## Support

For issues and questions:
- Check logs: `docker compose -f docker-compose.prod.yml logs`
- Review documentation
- Open GitHub issue

## Commands Reference

```bash
# Development
docker compose up -d                    # Start dev
docker compose down                     # Stop dev

# Production
docker compose -f docker-compose.prod.yml build    # Build
docker compose -f docker-compose.prod.yml up -d    # Start
docker compose -f docker-compose.prod.yml down     # Stop
docker compose -f docker-compose.prod.yml logs -f  # Logs
docker compose -f docker-compose.prod.yml ps       # Status
```
