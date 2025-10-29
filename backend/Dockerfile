# Multi-stage build for better optimization
FROM python:3.10-alpine3.18 AS builder

# Install system dependencies for building
RUN apk add --update --no-cache \
    gcc \
    libc-dev \
    libffi-dev \
    openssl-dev \
    libtool \
    m4 \
    g++ \
    autoconf \
    automake \
    postgresql-dev \
    build-base

# Set environment variables
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VENV_IN_PROJECT=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

# Install poetry
RUN pip install --upgrade pip && pip install poetry

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml pyproject.toml
COPY poetry.lock ./

# Install dependencies only (no project installation)
RUN poetry install --only=main --no-root \
    && rm -rf $POETRY_CACHE_DIR

# Production stage
FROM python:3.10-alpine3.18 AS production

# Install runtime dependencies and build deps (for compiling wheels)
RUN apk add --update --no-cache \
    postgresql-libs \
    libffi \
    openssl \
    build-base \
    postgresql-dev \
    libffi-dev \
    openssl-dev \
    bash \
    gcc \
    musl-dev \
    libc-dev

# Create non-root user
RUN adduser -D -s /bin/sh app

# Set work directory
WORKDIR /srv

# Install poetry
RUN pip install --upgrade pip && pip install poetry

# Create necessary directories and set permissions (run as root)
RUN mkdir -p /var/run/celery && \
    chown -R app:app /var/run/celery /srv

# Switch to non-root user
USER app

# Copy dependency files and install (with venv)
COPY pyproject.toml pyproject.toml
COPY poetry.lock ./

RUN poetry install --only=main --no-root

# Copy application code
COPY --chown=app:app src ./src
COPY --chown=app:app migrations ./migrations
COPY --chown=app:app run_seed.py ./run_seed.py
COPY --chown=app:app prepare_data ./prepare_data
ADD filesystem /

# Switch back to root to set file permissions
USER root
RUN chmod +x /entrypoints/web.sh
USER app

# Set environment variables
ENV FLASK_APP=src/entry:flask_app
ENV PYTHONPATH=/srv

# Create necessary directories (no-op if already exists)
RUN mkdir -p /var/run/celery

# Expose port
EXPOSE 8080

# Set default command
CMD ["/entrypoints/web.sh"]
