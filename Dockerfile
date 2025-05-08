FROM python:3.13.3-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    DJANGO_ENVIRONMENT=build

# Install system dependencies (uncomment and modify if required)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Install uv for dependency management
RUN pip install uv

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project \
    --group pg --group storages --group web

# Copy and install the project
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev \
    --group pg --group storages --group web

# Production image
FROM python:3.13-slim AS production

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
RUN useradd -m -s /bin/bash app && chown -R app:app /app

# Copy installed packages and app files from the builder image
COPY --from=builder --chown=app:app /app /app

# Run as non-root user
USER app

# Start Granian server
CMD ["granian", "config.asgi:application"]
