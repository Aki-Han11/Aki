# EBook Store

A full-stack e-book store web application with user management, book browsing, shopping cart, orders, favorites, ratings, and an admin panel with recommendation engine.

**Tech Stack**: Vue 3 (Vite) + Django REST Framework + SQLite + JWT Authentication

---

## Quick Start (Choose One)

### Option A: Docker — Zero Environment Setup 🐳

*Requires only Docker Desktop installed*

```bash
docker compose up
```

Then open **http://localhost:8080** in your browser.

> This single command builds the frontend, installs Python dependencies, runs migrations, and starts the server — all automatically.

### Option B: Python Only — One Command 🐍

*Requires Python 3.10+ installed*

```bash
# Terminal 1 — Backend (serves both API and frontend)
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8080
```

Then open **http://localhost:8080** in your browser.

> The frontend is already built in `frontend/dist/`. Django serves it as static files — no Node.js needed!

### Option C: Development Mode (Full Dev Setup)

*Requires Python 3.10+ and Node.js 18+*

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8080

# Terminal 2 — Frontend (with hot-reload)
cd frontend
npm install
npm run dev
```

Then open **http://localhost:5173** (Vite dev server proxies API calls).

---

## Demo Accounts

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | `admin`  | `admin123` |
| User  | `demo`   | `demo123`  |

---

## Features

### User Side
- 📚 Browse, search, and filter e-books by category
- ❤️ Add/remove favorites
- 🛒 Shopping cart with order placement
- ⭐ Rate and review purchased books
- 📥 Download purchased e-books
- 👤 User profile management
- 🔐 JWT-based authentication

### Admin Panel (`/admin` route after login as admin)
- 📊 Dashboard with sales statistics
- 📖 Manage books and categories
- 👥 User management
- 🤖 Recommendation engine (KNN-based collaborative filtering)

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `POST /api/register/` | POST | User registration |
| `POST /api/login/` | POST | User login (returns JWT) |
| `GET /api/me/` | GET | Current user profile |
| `GET /api/books/` | GET | List books (paginated) |
| `GET /api/books/{id}/` | GET | Book details |
| `GET /api/books/?search=keyword` | GET | Search books |
| `GET /api/categories/` | GET | List categories |
| `POST /api/favorites/` | POST | Add favorite |
| `GET /api/favorites/` | GET | List favorites |
| `GET /api/cart/` | GET | View cart |
| `POST /api/orders/` | POST | Place order |
| `GET /api/orders/` | GET | Order history |
| `POST /api/ratings/` | POST | Rate a book |
| `GET /api/downloads/` | GET | Download history |
| `GET /api/admin/dashboard/` | GET | Admin dashboard |

All protected endpoints require: `Authorization: Bearer <token>`

---

## Project Structure

```
ebook-platform/
├── backend/
│   ├── config/          # Django settings & root URL conf
│   ├── users/           # Custom user model & auth
│   ├── books/           # Book & category management
│   ├── cart/            # Shopping cart
│   ├── orders/          # Order processing
│   ├── favorites/       # User favorites
│   ├── ratings/         # Book ratings & reviews
│   ├── downloads/       # Purchase download tracking
│   ├── recommendations/ # ML-based book recommendations
│   ├── admin_panel/     # Admin dashboard APIs
│   ├── manage.py        # Django management script
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/         # Axios config & API endpoints
│   │   ├── components/  # Reusable Vue components
│   │   ├── layouts/     # Page layouts
│   │   ├── router/      # Vue Router config
│   │   ├── store/       # Pinia state management
│   │   └── views/       # Page components
│   ├── dist/            # Built frontend (served by Django)
│   └── package.json     # Node dependencies
├── Dockerfile           # Multi-stage Docker build
└── README.md
```

---

## Notes for the Professor

1. **Database**: Uses SQLite (`backend/db.sqlite3`) — no database server setup required. The demo database comes pre-loaded with sample books, users, and data.

2. **How the frontend is served**: In production mode, Django's `TemplateView` serves the Vue SPA's `index.html` for all non-API routes. Static assets (JS/CSS) are served via Django's static file system from `frontend/dist/assets/`.

3. **Recommendation engine**: Uses `scikit-surprise` with KNNBaseline algorithm. Train it via the admin panel after enough ratings are accumulated.

4. **Authentication**: JWT tokens (24h access + 7d refresh). Tokens are stored in `localStorage` and automatically attached to API requests.

---

## Build Frontend (If You Modify It)

```bash
cd frontend
npm install
npm run build
```

The built files go to `frontend/dist/` and Django picks them up automatically on next restart.
