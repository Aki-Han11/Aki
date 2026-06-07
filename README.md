# EBookStore

Full-stack e-book platform — browse, purchase, download, and discover books through smart recommendations.

**🔗 Live Demo:** [https://aki-production-1fb1.up.railway.app](https://aki-production-1fb1.up.railway.app)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vue 3 + Vite + Element Plus + Pinia + Vue Router |
| **Backend** | Django 6.0 + Django REST Framework |
| **Auth** | JWT (SimpleJWT) |
| **Database** | SQLite (dev) / PostgreSQL (production) |
| **ML Engine** | scikit-surprise (KNNBaseline collaborative filtering) |
| **Container** | Docker (multi-stage) |
| **Cloud** | Railway |

---

## Quick Start

```bash
# Docker (recommended)
docker compose up

# Or Python only
cd backend && pip install -r requirements.txt
python manage.py migrate && python manage.py seed_data
python manage.py runserver 8080
```

Open **http://localhost:8080** (or **http://localhost:5173** with `npm run dev` in `frontend/`).

---

## Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `demo` | `demo123` |

---

## Features

- 📚 Browse, search, and filter books by category
- 🔥 Popular rankings weighted by purchases, favorites, and views
- 🤖 Personalized recommendations (KNN collaborative filtering)
- ❤️ Favorites · 🛒 Shopping cart · 📦 Order management
- ⭐ Rate & review purchased books (1-5 stars)
- 📥 Download purchased e-books
- 👤 User profile with password management
- 📊 Admin dashboard with stats, CRUD, and ML model training

---

## Project Structure

```
ebook-platform/
├── frontend/                          # Vue 3 SPA
│   └── src/
│       ├── components/                # BookGrid, LandingNav
│       ├── layouts/                   # MainLayout, AdminLayout
│       ├── router/                    # Auth-guarded routes
│       ├── store/                     # Pinia (auth, cart)
│       ├── views/                     # 16 page components
│       └── api/                       # Axios + endpoints
├── backend/
│   ├── books/                         # Book & Category models
│   ├── users/                         # Custom User + JWT auth
│   ├── cart/                          # Shopping cart
│   ├── orders/                        # Order workflow
│   ├── favorites/                     # User favorites
│   ├── ratings/                       # Star ratings + reviews
│   ├── downloads/                     # Download tracking
│   ├── recommendations/               # KNN training & prediction
│   └── admin_panel/                   # Admin APIs
├── Dockerfile
└── docker-compose.yml
```

---

**Author:** HAN QI · **Course:** AI Full-Stack Development · **Date:** June 2026
