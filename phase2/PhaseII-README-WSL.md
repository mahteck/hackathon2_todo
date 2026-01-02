# Phase II - Full-Stack Web Todo App

Complete full-stack web application for the Evolution of Todo project. This phase transforms the console app from Phase I into a modern web application with a Next.js frontend and FastAPI backend.

## Overview

- **Backend:** FastAPI + SQLModel + async PostgreSQL/SQLite
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS
- **DB:** PostgreSQL (prod) or SQLite (dev/testing)
- **Architecture:** Clean, service-layer driven
- **Features:** CRUD, priorities, tags, filters, sorting, due dates

> **Environment:** All instructions are designed for  
> 🟢 Ubuntu on WSL (`Windows Subsystem for Linux`)

Project root path assumed:

/mnt/d/Data/GIAIC/hackathon2/phase2

---

# 🚀 Quick Start Options

## ✅ Option 1 — Docker Compose (if Docker Installed)

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2
docker-compose up
```

```bash
 Terminal 1 - Backend:
  cd /mnt/d/Data/GIAIC/hackathon2/phase2/backend
  # Make sure .env has the JSON array format (already fixed)
  python3 -m venv .venv
  source .venv/bin/activate  # Windows: .venv\Scripts\activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload

```

Services:
- Frontend → http://localhost:3000
- Backend API → http://localhost:8000
- Docs → http://localhost:8000/docs

Stop:
```bash
docker-compose down
```

---

## ✅ Option 2 — Manual Run (Recommended now)

Run:
- Backend in Terminal 1
- Frontend in Terminal 2

---

# 🛠 Backend Setup (FastAPI)

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

SQLite (dev default) in `.env`:
```
DATABASE_URL=sqlite+aiosqlite:///./dev.db
```

---

# 🎨 Frontend Setup (Next.js 14 + TS)

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2/frontend
npm install
npm run dev
```

Open:
- http://localhost:3000

---

# 🧪 Tests

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2/backend
source .venv/bin/activate
pytest -v
```

Coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

---

# 🌱 Seed Data (optional)

```bash
cd /mnt/d/Data/GIAIC/hackathon2/phase2/backend
source .venv/bin/activate
python3 scripts/seed_data.py
```

---

# 🧭 Milestones

Backend running:
```bash
uvicorn app.main:app --reload
```

Frontend running:
```bash
npm run dev
```

---

# ⚠ Known limits

- single user
- no auth yet
- sqlite default
- no realtime

---

# 🎯 Phase III

- auth/JWT
- multi-user
- realtime
- sharing
- recurring tasks
