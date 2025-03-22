FROM python:3.13-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    SECRET_KEY=build-time-value-that-does-not-matter \
    DEBUG=True

# Install uv for dependency management
RUN pip install uv

# Create app directory
WORKDIR /app

# Copy requirements files
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN uv pip install --group web --group pg --system .

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Production image
FROM python:3.13-slim AS production

WORKDIR /app

# Copy installed packages and app from base image
COPY --from=base /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=base /usr/local/bin/granian /usr/local/bin/
COPY --from=base /app /app

# Run as non-root user
RUN useradd -m -s /bin/bash app && chown -R app:app /app
USER app

# Start Granian server
CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "8000", "config.asgi:application"]
