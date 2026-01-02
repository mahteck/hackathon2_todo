# 🚀 Git & Build Checklist - Before Commit

## ✅ Files That Should NOT Be Committed

### 🔒 Sensitive Files (Already in .gitignore)
```
✅ backend/.env                    # Contains DATABASE_URL with password
✅ backend/test.db                 # SQLite database file
✅ .env.production                 # Production secrets
✅ .env.prod                       # Production environment
```

### 📦 Build & Dependencies (Already in .gitignore)
```
✅ node_modules/                   # Frontend dependencies (huge!)
✅ __pycache__/                    # Python bytecode
✅ .venv/                          # Python virtual environment
✅ .next/                          # Next.js build output
✅ build/, dist/                   # Build artifacts
```

### 💻 IDE & OS Files (Already in .gitignore)
```
✅ .vscode/                        # VS Code settings
✅ .idea/                          # PyCharm/IntelliJ
✅ .DS_Store                       # macOS
✅ *.swp, *.swo                    # Vim swap files
```

---

## ✅ Files That SHOULD Be Committed

### 📝 Configuration Templates
```
✅ backend/.env.example            # Template for .env
✅ .env.production                 # Template (without secrets)
✅ docker-compose.yml              # Development setup
✅ docker-compose.prod.yml         # Production setup
```

### 🐳 Docker Files
```
✅ backend/Dockerfile              # Development backend
✅ backend/Dockerfile.prod         # Production backend
✅ frontend/Dockerfile             # Development frontend
✅ frontend/Dockerfile.prod        # Production frontend
✅ .dockerignore (if exists)       # Docker ignore rules
```

### 📚 Documentation
```
✅ README.md
✅ PRODUCTION_GUIDE.md
✅ DBeaver_Connection_Guide.md
✅ COMPLETE_SETUP_SUMMARY.md
✅ GIT_BUILD_CHECKLIST.md
```

### 💾 Source Code
```
✅ backend/**/*.py                 # Python source files
✅ frontend/**/*.tsx, *.ts         # TypeScript/React files
✅ frontend/**/*.css               # Stylesheets
✅ backend/requirements.txt        # Python dependencies
✅ frontend/package.json           # Node dependencies
```

---

## 🔍 Pre-Commit Verification

### 1. Check What's Being Committed
```bash
# View status
git status

# View untracked files
git ls-files --others --exclude-standard

# Check if sensitive files are staged
git status | grep -E "\.env$|\.db$|node_modules|__pycache__"
```

### 2. Verify .gitignore is Working
```bash
# Test if .env would be ignored
git check-ignore -v backend/.env
# Should output: backend/.gitignore:... backend/.env

# Test if test.db would be ignored
git check-ignore -v backend/test.db
# Should output: .gitignore:... backend/test.db
```

### 3. Check File Sizes
```bash
# Find large files (>1MB) that might be committed
find . -type f -size +1M -not -path "*/node_modules/*" -not -path "*/.next/*" -not -path "*/.git/*"

# Should NOT show any .db files or build artifacts
```

---

## 📦 Build Verification

### Development Build
```bash
# Backend - Check requirements
cd backend
pip install -r requirements.txt

# Frontend - Check dependencies
cd ../frontend
npm install

# Run build test
npm run build
```

### Production Build
```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Should complete without errors
# Images should be created:
#   - phase2-backend:latest
#   - phase2-frontend:latest
```

---

## 🚨 Critical Checks Before Push

### Security Checklist
- [ ] No `.env` files in git status
- [ ] No database files (*.db) in git status
- [ ] No passwords or secrets in committed files
- [ ] `.env.example` has placeholder values (not real passwords)
- [ ] No `node_modules/` directory tracked
- [ ] No `__pycache__/` directories tracked

### Build Checklist
- [ ] Development build works: `npm run build` (frontend)
- [ ] Production build works: `docker compose -f docker-compose.prod.yml build`
- [ ] No build errors or warnings
- [ ] All imports resolve correctly
- [ ] TypeScript compiles without errors

### Documentation Checklist
- [ ] README.md updated
- [ ] PRODUCTION_GUIDE.md included
- [ ] DBeaver_Connection_Guide.md included
- [ ] All setup instructions clear

---

## 🎯 Git Commands for Clean Commit

### If Starting Fresh (First Time)
```bash
# Initialize git (if not done)
git init

# Add all files (gitignore will exclude sensitive ones)
git add .

# Verify what's being added
git status

# Check that .env and .db are NOT in the list
git status | grep -E "\.env$|\.db$" && echo "⚠️ WARNING: Sensitive files detected!" || echo "✅ Safe to commit"

# Create first commit
git commit -m "Initial commit: Todo App Phase 2 with Docker setup"
```

### If Continuing Existing Repo
```bash
# Check current status
git status

# Add specific files
git add .gitignore
git add backend/ frontend/
git add docker-compose*.yml
git add *.md

# Verify
git status

# Commit
git commit -m "feat: Add production build and documentation"
```

### If .env Was Accidentally Committed Before
```bash
# Remove from git but keep file
git rm --cached backend/.env
git rm --cached backend/test.db

# Add to .gitignore (already done)
# Commit the removal
git commit -m "fix: Remove sensitive files from git tracking"
```

---

## 🌐 Remote Push Checklist

### Before First Push
```bash
# Set remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/todo-app-phase2.git

# Verify remote
git remote -v

# Push to main branch
git push -u origin main
```

### Verify on GitHub/GitLab
After pushing, check on GitHub:
- [ ] No `.env` files visible
- [ ] No `.db` files visible
- [ ] No `node_modules/` directory
- [ ] Documentation files present
- [ ] Dockerfile.prod files present

---

## 🔧 Build Command Reference

### Development
```bash
# Start development environment
docker compose up -d

# Stop
docker compose down
```

### Production
```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Start production
docker compose -f docker-compose.prod.yml up -d

# Stop production
docker compose -f docker-compose.prod.yml down
```

### Testing Builds Locally
```bash
# Test backend build
docker build -f backend/Dockerfile.prod -t test-backend backend/

# Test frontend build
docker build -f frontend/Dockerfile.prod -t test-frontend frontend/

# Clean up test images
docker rmi test-backend test-frontend
```

---

## ✅ Final Pre-Commit Command

Run this before committing:
```bash
echo "🔍 Checking for sensitive files..."
git status | grep -E "\.env$|\.db$|node_modules|__pycache__" && echo "❌ STOP: Sensitive files detected!" || echo "✅ Safe to commit"

echo ""
echo "📊 Files to be committed:"
git status --short

echo ""
echo "📦 Testing production build..."
docker compose -f docker-compose.prod.yml build 2>&1 | grep -E "Successfully|ERROR" | tail -5
```

---

## 🎉 Success Criteria

Your repository is ready when:
- ✅ No sensitive files tracked
- ✅ Production build succeeds
- ✅ Documentation complete
- ✅ `.gitignore` files in place
- ✅ All teammates can clone and build

---

**Last Updated:** January 2, 2026
**Status:** Ready for Git Commit ✅
