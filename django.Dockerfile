# django.Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Django settings module
ENV DJANGO_SETTINGS_MODULE=djangotres.settings

# Collect static files for WhiteNoise
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "djangotres.wsgi:application", "--bind", "0.0.0.0:8000"]
