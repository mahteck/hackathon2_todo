@echo off
echo ========================================
echo    Git Fix Script - Fixing Issues
echo ========================================
echo.

echo Step 1: Removing .venv from git tracking...
git rm -r --cached phase1\.venv 2>nul
echo Done.
echo.

echo Step 2: Adding configuration files...
git add .gitignore
git add .gitattributes
git add phase1\.gitignore
git add phase2\.gitignore
git add phase2\backend\.gitignore
git add phase2\frontend\.gitignore
echo Done.
echo.

echo Step 3: Checking current status...
git status --short
echo.

echo ========================================
echo Next Steps:
echo 1. Review the files above
echo 2. If looks good, run: git add phase2/
echo 3. Then run: git add *.md
echo 4. Finally commit: git commit -m "feat: Add Phase 2"
echo ========================================
pause
