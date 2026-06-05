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

# Install system dependencies (if needed for scikit-surprise)
RUN pip install --no-cache-dir --upgrade pip

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
RUN mkdir -p /app/frontend
COPY --from=frontend /app/frontend/dist /app/frontend/dist

# Run migrations and start server
EXPOSE 8080
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]
