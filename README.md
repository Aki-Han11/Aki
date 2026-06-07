# EBookStore

A full-stack e-book platform — browse, purchase, download, and discover books through smart recommendations. Built with Vue 3 + Django REST Framework.

**🔗 Live Demo:** [https://aki-production-1fb1.up.railway.app](https://aki-production-1fb1.up.railway.app)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vue 3 (Composition API) + Vite + Element Plus + Pinia + Vue Router |
| **Backend** | Django 6.0 + Django REST Framework |
| **Auth** | JWT (SimpleJWT) — 24h Access Token + 7d Refresh Token |
| **Database (Dev)** | SQLite |
| **Database (Prod)** | PostgreSQL (Railway managed) |
| **WSGI Server** | Gunicorn 23.0 (3 workers) |
| **Static Files** | WhiteNoise (compressed, cached) |
| **ML Engine** | scikit-surprise (KNNBaseline collaborative filtering) |
| **Container** | Docker (multi-stage: Node.js → Python) |
| **Cloud** | Railway |

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

### Docker (Recommended)

```bash
docker compose up
```

Open **http://localhost:8080**. Builds frontend, installs deps, runs migrations, seeds data, starts server — all in one command.

### Python Only (No Node.js)

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver 8080
```

Open **http://localhost:8080**. Frontend is pre-built in `frontend/dist/`, served by WhiteNoise.

### Full Dev Setup (Hot Reload)

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver 8080

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** (Vite proxies API to :8080).

---

## Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `demo` | `demo123` |

---

## Features

### Reader Experience
- 📚 **Browse & Search** — full-text search by title, author, keyword; filter by category
- 🔥 **Popular Rankings** — weighted by purchases, favorites, and views
- 🆕 **New Arrivals** — latest additions to the collection
- 🤖 **Smart Recommendations** — KNN collaborative filtering, personalized per user
- ❤️ **Favorites** — save books you love
- 🛒 **Shopping Cart** — add books, manage quantities
- 📦 **Orders** — checkout, pay, track status (pending → paid → completed)
- ⭐ **Ratings & Reviews** — rate purchased books 1-5 stars, write reviews
- 📥 **Downloads** — download purchased e-books, view download history
- 👤 **Profile** — manage email, change password

### Admin Panel (`/admin` — admin login required)
- 📊 **Dashboard** — total users, books, orders, revenue; top-selling books table
- 📖 **Book Management** — full CRUD for books (title, author, price, cover, tags, stock)
- 📂 **Category Management** — create and manage book categories
- 👥 **User Management** — search users, view profiles, manage accounts
- 🤖 **Recommendation Engine** — one-click model training with result stats

---

## UI Design System

The frontend follows a unified, editorial design language across all pages:

### Layout Architecture
| Component | Scope | Description |
|-----------|-------|-------------|
| `LandingNav` | Homepage only | Minimal glassmorphism nav — brand logo + user actions |
| `MainLayout` | All inner pages | Sticky header with custom nav links + search + user menu |
| `AdminLayout` | Admin pages | Dark sidebar + warm content area |

### Design Philosophy
- **Warm ivory palette** (`#fefcf8` base) — clean, inviting, consistent across all pages
- **Editorial typography** — Inter for body, Playfair Display italic for brand
- **De-modularized** — content separated by whitespace and subtle dividers, not heavy card borders
- **Left-aligned titles** — unified page header layout
- **Horizontal book rows** — cover | info | description | price layout on list pages
- **Custom SVG icons** — consistent stroke-width, modern minimalist style

### Pages
| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Hero with gradient, smart discovery cards, popular & recommended books |
| Browse | `/books` | Full book catalog with search, category filter, pagination |
| Book Detail | `/books/:id` | Cover, metadata, purchase, favorite, review, recommendations |
| Popular | `/hot` | Most popular books ranked by engagement |
| Recommended | `/recommended` | Personalized picks (requires login) |
| Search | `/search?q=` | Full-text search results |
| Cart | `/cart` | Shopping cart with checkout |
| Favorites | `/favorites` | Saved books |
| Orders | `/orders` | Order history |
| Order Detail | `/orders/:id` | Single order with items and actions |
| Downloads | `/downloads` | Download history |
| Profile | `/profile` | Edit email, change password |
| Login | `/login` | JWT authentication |
| Register | `/register` | New account creation |
| Admin Dashboard | `/admin` | Stats and top sellers |
| Admin Books | `/admin/books` | Book CRUD |
| Admin Categories | `/admin/categories` | Category CRUD |
| Admin Users | `/admin/users` | User management |
| Admin Recommendations | `/admin/recommendations` | Train ML model |

---

## API Reference

### Public Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/register/` | Create account |
| `POST` | `/api/login/` | Get JWT tokens |
| `GET` | `/api/books/` | List books (paginated, `?search=&category=`) |
| `GET` | `/api/books/{id}/` | Book detail |
| `GET` | `/api/books/hot/?period=all\|week\|day` | Hot ranked books |
| `GET` | `/api/books/new/` | New arrivals |
| `GET` | `/api/categories/` | All categories |

### Authenticated Endpoints (`Authorization: Bearer <token>`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/me/` | Current user profile |
| `PUT` | `/api/me/` | Update profile |
| `PUT` | `/api/me/password/` | Change password |
| `GET` | `/api/books/recommend/` | Personalized recommendations |
| `GET` | `/api/books/{id}/download/` | Download purchased book |
| `GET` | `/api/cart/` | View cart |
| `POST` | `/api/cart/` | Add to cart |
| `DELETE` | `/api/cart/{id}/` | Remove from cart |
| `POST` | `/api/cart/checkout/` | Checkout entire cart |
| `GET` | `/api/favorites/` | List favorites |
| `POST` | `/api/favorites/` | Add favorite |
| `DELETE` | `/api/favorites/{id}/` | Remove favorite |
| `GET` | `/api/orders/` | Order history |
| `POST` | `/api/orders/` | Place single-book order |
| `GET` | `/api/orders/{id}/` | Order detail |
| `PUT` | `/api/orders/{id}/pay/` | Simulate payment |
| `PUT` | `/api/orders/{id}/cancel/` | Cancel order |
| `POST` | `/api/ratings/` | Rate & review a book |
| `GET` | `/api/books/{id}/reviews/` | All reviews for a book |
| `GET` | `/api/downloads/` | Download history |

### Admin Endpoints (Admin role required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/admin/stats/` | Dashboard statistics |
| `GET/POST` | `/api/admin/books/` | List / create books |
| `GET/PUT/DELETE` | `/api/admin/books/{id}/` | Manage single book |
| `GET/POST` | `/api/admin/categories/` | List / create categories |
| `GET/PUT/DELETE` | `/api/admin/categories/{id}/` | Manage single category |
| `GET` | `/api/admin/users/` | List users |
| `GET/PUT` | `/api/admin/users/{id}/` | View / update user |
| `POST` | `/api/admin/train/` | Train recommendation model |

---

## Recommendation Engine

**Algorithm:** User-Based Collaborative Filtering via KNNBaseline (scikit-surprise)

- **Metric:** Pearson Baseline — accounts for user/item rating biases
- **Neighborhood:** k = 40 nearest users
- **Training:** Admin-triggered; model serialized to `model.pkl`
- **Prediction:** Top-12 unrated books per user
- **Cold start:** Random picks for unauthenticated users; model requires ≥ 5 ratings

**Hot Score Formula:**
```
Hot Score = views×1 + favorites×3 + purchases×5 + downloads×2
```

---

## Project Structure

```
ebook-platform/
├── frontend/                          # Vue 3 + Vite SPA
│   ├── index.html                     # Entry HTML (Inter + Playfair Display fonts)
│   ├── vite.config.js                 # Vite config with API proxy
│   ├── src/
│   │   ├── App.vue                    # Global styles & CSS reset
│   │   ├── main.js                    # App bootstrap (Element Plus, Pinia, Router)
│   │   ├── api/
│   │   │   ├── index.js               # Axios instance with JWT interceptor
│   │   │   └── endpoints.js           # All API call functions
│   │   ├── components/
│   │   │   ├── BookGrid.vue           # Reusable book card grid (no borders, image-forward)
│   │   │   └── LandingNav.vue         # Homepage nav — Playfair brand + user actions
│   │   ├── layouts/
│   │   │   ├── MainLayout.vue         # Inner page layout — sticky header + custom nav
│   │   │   └── AdminLayout.vue        # Admin layout — dark sidebar + warm content
│   │   ├── router/
│   │   │   └── index.js               # Vue Router with auth/admin route guards
│   │   ├── store/
│   │   │   ├── auth.js                # Pinia auth store (login, logout, JWT refresh)
│   │   │   └── cart.js                # Pinia cart store (badge count)
│   │   └── views/
│   │       ├── HomePage.vue           # Landing page — hero + discovery + books + footer
│   │       ├── BookListPage.vue       # Browse all books with filters
│   │       ├── BookDetailPage.vue     # Book detail, buy, favorite, review, related
│   │       ├── FeaturedPage.vue       # Popular / Recommended / New Arrivals lists
│   │       ├── SearchPage.vue         # Search results
│   │       ├── LoginPage.vue          # JWT login form
│   │       ├── RegisterPage.vue       # Registration form
│   │       ├── ProfilePage.vue        # User profile — avatar, info, password
│   │       ├── CartPage.vue           # Shopping cart with checkout
│   │       ├── FavoritesPage.vue      # Saved books list
│   │       ├── OrdersPage.vue         # Order history
│   │       ├── OrderDetailPage.vue    # Single order with items & actions
│   │       ├── DownloadsPage.vue      # Download history
│   │       └── admin/
│   │           ├── DashboardPage.vue  # Admin stats & top sellers
│   │           ├── BooksPage.vue      # Book CRUD
│   │           ├── CategoriesPage.vue # Category CRUD
│   │           ├── UsersPage.vue      # User management
│   │           └── RecommendationsPage.vue  # ML model training
│   └── dist/                          # Production build (committed for Python-only mode)
├── backend/
│   ├── config/                        # Django settings, URLs, WSGI/ASGI
│   ├── users/                         # Custom User model + JWT auth views
│   ├── books/                         # Book & Category models, search, ranking, seeding
│   ├── cart/                          # Cart model (unique per user+book)
│   ├── orders/                        # Order workflow (pending→paid→completed, cancel)
│   ├── favorites/                     # User favorites (unique per user+book)
│   ├── ratings/                       # 1-5 star ratings + text reviews
│   ├── downloads/                     # Download tracking
│   ├── recommendations/               # KNN training (train.py) & prediction (predict.py)
│   ├── admin_panel/                   # Admin dashboard stats & management APIs
│   ├── manage.py
│   └── requirements.txt
├── Dockerfile                         # Multi-stage: Node build → Python serve
├── docker-compose.yml                 # Single-command local deployment
├── railway.json                       # Railway deployment config
└── README.md
```

---

## Deployment (Railway)

1. Push to `main` → Railway auto-detects `Dockerfile`
2. PostgreSQL service attached → `DATABASE_URL` injected
3. On startup: `migrate` → `seed_data` → `gunicorn` (prod) or `runserver` (dev)
4. Health check: `GET /api/books/?page=1`

**Auto-detection:** If `DATABASE_URL` exists → production mode (gunicorn). Otherwise → development mode (runserver).

---

## Rebuilding Frontend

```bash
cd frontend
npm install
npm run build
```

Outputs to `frontend/dist/` — Django serves it on next restart.

---

**Author:** HAN QI  
**Course:** AI Full-Stack Development  
**Date:** June 2026
