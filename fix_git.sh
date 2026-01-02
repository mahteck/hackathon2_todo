#!/bin/bash

echo "🔧 Fixing Git Issues..."
echo ""

# Remove .venv from git cache if it exists
echo "1. Removing .venv from git tracking..."
git rm -r --cached phase1/.venv 2>/dev/null || echo "   .venv not in git cache"
git rm -r --cached phase2/backend/.venv 2>/dev/null || echo "   backend/.venv not in git cache"

echo ""
echo "2. Removing any accidentally tracked files..."
git rm --cached phase1/.venv/bin/python 2>/dev/null || echo "   python symlink not in cache"

echo ""
echo "3. Adding .gitignore and .gitattributes..."
git add .gitignore
git add .gitattributes

echo ""
echo "4. Updating phase1 and phase2 .gitignore..."
git add phase1/.gitignore
git add phase2/.gitignore
git add phase2/backend/.gitignore
git add phase2/frontend/.gitignore

echo ""
echo "✅ Git fixed! Now you can safely run: git add ."
