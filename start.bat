@echo off
chcp 65001 >nul
title EBook Store - Starting...

echo ============================================
echo   EBook Store - One-Click Startup
echo ============================================
echo.

set "BASE_DIR=%~dp0"

echo [1/3] Starting Django backend...
start "EBook Backend" cmd /k "cd /d "%BASE_DIR%backend" && python manage.py runserver 8080"
echo   Backend starting on http://localhost:8080

timeout /t 3 /nobreak >nul

echo [2/3] Starting Vue frontend...
start "EBook Frontend" cmd /k "cd /d "%BASE_DIR%frontend" && npx vite --port 5173"
echo   Frontend starting on http://localhost:5173

timeout /t 3 /nobreak >nul

echo [3/3] Opening browser...
start http://localhost:5173

echo.
echo ============================================
echo   EBook Store is running!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8080
echo.
echo   Demo accounts:
echo     Admin - admin / admin123
echo     User  - demo  / demo123
echo ============================================
echo.
echo Close the two terminal windows to stop.
pause
