#!/bin/bash

echo "============================================"
echo "  EBook Store - One-Click Startup"
echo "============================================"
echo ""

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/3] Starting Django backend..."
cd "$BASE_DIR/backend"
python manage.py runserver 8080 &
BACKEND_PID=$!
echo "  Backend starting on http://localhost:8080 (PID: $BACKEND_PID)"

sleep 3

echo "[2/3] Starting Vue frontend..."
cd "$BASE_DIR/frontend"
npx vite --port 5173 &
FRONTEND_PID=$!
echo "  Frontend starting on http://localhost:5173 (PID: $FRONTEND_PID)"

sleep 3

echo "[3/3] Opening browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
elif command -v open &> /dev/null; then
    open http://localhost:5173
fi

echo ""
echo "============================================"
echo "  EBook Store is running!"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8080"
echo ""
echo "  Demo accounts:"
echo "    Admin - admin / admin123"
echo "    User  - demo  / demo123"
echo "============================================"
echo ""
echo "Press Ctrl+C to stop all services."

# Cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Done."
}
trap cleanup EXIT

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
