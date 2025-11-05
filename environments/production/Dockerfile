FROM python:3.12-slim-trixie as python-base

ARG PORT=8000
ENV PORT=${PORT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

FROM python-base AS base

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    netcat-traditional \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app

# 임시 디렉토리 생성 (import_export용)
RUN mkdir -p /app/tmp && chmod 777 /app/tmp

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM base AS builder

# Build dependencies only in builder stage
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Git configuration
RUN git config --global url."https://".insteadOf git:// && \
    git config --global url."https://".insteadOf ssh://git@

COPY pyproject.toml uv.lock /_lock/

RUN --mount=type=cache,target=/root/.cache \
  cd /_lock/ && \
  uv sync --frozen --no-install-project

FROM base AS runtime

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

WORKDIR /app/webapp

COPY ./webapp /app/webapp

# Clean up Python bytecode and cache
RUN find /app -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find /app -type f -name "*.pyc" -delete 2>/dev/null || true

ENV PATH="/app/.venv/bin:$PATH"

COPY ./environments/production/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

EXPOSE ${PORT}
