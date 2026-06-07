# EBook Store

A full-stack e-book online shopping platform built with AI-assisted development. Features user authentication, book browsing/search, shopping cart, order processing, favorites, ratings, KNN-based recommendation engine, and an admin dashboard.

**🔗 Live Demo:** [https://aki-production-1fb1.up.railway.app](https://aki-production-1fb1.up.railway.app)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vue 3 (Composition API) + Vite + Element Plus + Pinia + Vue Router |
| **Backend** | Django 6.0 + Django REST Framework |
| **Auth** | JWT (SimpleJWT) — 24h Access Token + 7d Refresh Token |
| **Database (Dev)** | SQLite |
| **Database (Production)** | PostgreSQL (Railway managed) |
| **WSGI Server** | Gunicorn 23.0 (3 workers) |
| **Static Files** | WhiteNoise (compressed, cached) |
| **ML Engine** | scikit-surprise (KNNBaseline collaborative filtering) |
| **Containerization** | Docker (multi-stage build) |
| **Cloud Platform** | Railway |

---

## Architecture

```
Browser ──▶ https://aki-production-1fb1.up.railway.app
                    │
            ┌───────▼────────┐
            │  Railway Cloud  │
            │  ┌───────────┐  │
            │  │ Docker     │  │
            │  │ ┌───────┐ │  │
            │  │ │Gunicorn│ │  │
            │  │ │3 Worker│ │  │
            │  │ └───┬───┘ │  │
            │  │ ┌───▼───┐ │  │
            │  │ │Django │  │  │
            │  │ │+WhiteNoise│  │
            │  │ └───┬───┘ │  │
            │  └─────┼─────┘  │
            │  ┌─────▼─────┐  │
            │  │PostgreSQL │  │
            │  └───────────┘  │
            └─────────────────┘
```

---

## Quick Start

### Option A: Docker (Recommended)

Requires only Docker Desktop installed.

```bash
docker compose up
```

Open **http://localhost:8080**.

> This single command builds the frontend, installs Python dependencies, runs migrations, seeds demo data, and starts the server — all automatically.

### Option B: Python Only (No Node.js)

Requires Python 3.10+.

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver 8080
```

Open **http://localhost:8080**.

> The frontend is pre-built in `frontend/dist/`. Django serves it as static files via WhiteNoise.

### Option C: Full Dev Setup (Hot Reload)

Requires Python 3.10+ and Node.js 18+.

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver 8080

# Terminal 2 — Frontend (hot reload on :5173)
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** (Vite dev server proxies API to :8080).

---

## Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `demo` | `demo123` |

---

## Features

### User Side

- 📚 Browse, search (title/author/tags), and filter e-books by category
- 🔥 Hot rankings (all-time / this week / today)
- 🆕 New arrivals
- 🤖 Personalized recommendations (KNN collaborative filtering)
- ❤️ Add/remove favorites
- 🛒 Shopping cart with quantity management
- 📦 Order placement and status tracking (pending → paid → completed)
- ⭐ Rate and review purchased books (1-5 stars)
- 📥 Download purchased e-books
- 👤 User profile management
- 🔐 JWT-based authentication with auto-refresh

### Admin Panel (`/admin` route after admin login)

- 📊 Dashboard with sales statistics and top-selling books
- 📖 Manage books and categories (CRUD)
- 👥 User management (search, disable, role control)
- 🤖 Train recommendation model with one click

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/register/` | — | User registration |
| `POST` | `/api/login/` | — | Login (returns JWT access + refresh) |
| `GET` | `/api/me/` | JWT | Current user profile |
| `GET` | `/api/books/` | — | List books (paginated, ?category=&search=) |
| `GET` | `/api/books/{id}/` | — | Book details |
| `GET` | `/api/books/hot/?period=all\|week\|day` | — | Hot ranked books |
| `GET` | `/api/books/new/` | — | Newest arrivals |
| `GET` | `/api/books/recommend/` | — | Personalized recommendations |
| `GET` | `/api/books/{id}/download/` | JWT | Download purchased book |
| `GET` | `/api/categories/` | — | List categories |
| `GET` | `/api/cart/` | JWT | View cart |
| `POST` | `/api/cart/` | JWT | Add item to cart |
| `GET` | `/api/favorites/` | JWT | List favorites |
| `POST` | `/api/favorites/` | JWT | Add favorite |
| `GET` | `/api/orders/` | JWT | Order history |
| `POST` | `/api/orders/` | JWT | Place order |
| `PUT` | `/api/orders/{id}/pay/` | JWT | Simulate payment |
| `POST` | `/api/ratings/` | JWT | Rate a book |
| `GET` | `/api/downloads/` | JWT | Download history |
| `GET` | `/api/admin/stats/` | Admin | Dashboard statistics |
| `POST` | `/api/admin/train/` | Admin | Train recommendation model |

All protected endpoints require: `Authorization: Bearer <token>`

---

## Recommendation Engine

The platform uses **User-Based Collaborative Filtering** with the **KNNBaseline** algorithm (scikit-surprise):

- **Similarity metric:** Pearson Baseline (accounts for user/item rating biases)
- **Neighborhood:** k = 40 nearest users
- **Training:** Admin triggers training via the admin panel; model serialized to `model.pkl`
- **Prediction:** For each user, predicts ratings for unrated books and returns Top-12
- **Cold start:** Unauthenticated users receive random recommendations; model requires ≥5 ratings

**Hot Score formula:**

```
Hot Score = view_count × 1 + favorite_count × 3 + purchase_count × 5 + download_count × 2
```

---

## Project Structure

```
ebook-platform/
├── frontend/                  # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── api/               # Axios config & API endpoints
│   │   ├── components/        # Reusable Vue components (BookGrid, etc.)
│   │   ├── layouts/           # MainLayout, AdminLayout
│   │   ├── router/            # Vue Router with auth guards
│   │   ├── store/             # Pinia stores (auth, cart)
│   │   └── views/             # Page components (Home, Login, Cart, etc.)
│   ├── dist/                  # Built frontend (served by Django in production)
│   └── vite.config.js         # Vite configuration
├── backend/
│   ├── config/                # Django settings & root URL configuration
│   ├── users/                 # Custom User model (AbstractUser), JWT auth
│   ├── books/                 # Book & Category models, search, hot/new lists
│   ├── cart/                  # Shopping cart (unique per user+book)
│   ├── orders/                # Order processing (4-state workflow)
│   ├── favorites/             # User favorites (unique per user+book)
│   ├── ratings/               # 1-5 star ratings (feeds recommendation engine)
│   ├── downloads/             # Download history tracking
│   ├── recommendations/       # KNNBaseline training & prediction
│   ├── admin_panel/           # Admin dashboard APIs & permission checks
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
├── Dockerfile                 # Multi-stage build (Node.js → Python)
├── docker-compose.yml         # Single-command local deployment
└── README.md
```

---

## Deployment

This project is deployed on [Railway](https://railway.app) with automatic GitHub integration:

1. Push to `main` branch → Railway auto-detects Dockerfile → builds and deploys
2. PostgreSQL database service attached → `DATABASE_URL` auto-injected
3. Environment variables configured: `DEBUG=False`, `ALLOWED_HOSTS=.up.railway.app`
4. On startup: runs `migrate` → runs `seed_data` → starts `gunicorn` (production) or `runserver` (dev)

**Production vs Dev auto-detection:** The Dockerfile entrypoint checks for `DATABASE_URL` — if present, starts gunicorn in production mode; otherwise starts Django runserver for local development.

---

## Rebuild Frontend (After Modifications)

```bash
cd frontend
npm install
npm run build
```

Built files output to `frontend/dist/` — Django picks them up automatically on next restart.

---

**Author:** HAN QI  
**Course:** AI Full-Stack Development  
**Date:** June 2026
