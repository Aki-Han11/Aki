# Stage 1: Build Vue frontend
FROM node:22-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Django backend with built frontend
FROM python:3.12-slim
WORKDIR /app/backend

# Install Python deps — pip upgrade + requirements in one cached layer
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
RUN mkdir -p /app/backend/staticfiles /app/frontend
COPY --from=frontend /app/frontend/dist /app/frontend/dist

# Run migrations and start server
EXPOSE 8080

CMD ["sh", "-c", "\
  python manage.py migrate && \
  python manage.py seed_data && \
  if [ -n \"$DATABASE_URL\" ]; then \
    echo 'Production mode: gunicorn' && \
    gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3 --access-logfile -; \
  else \
    echo 'Dev mode: Django runserver' && \
    python manage.py runserver 0.0.0.0:${PORT:-8080}; \
  fi \
"]
