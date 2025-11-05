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
    build-essential \
    curl \
    wget \
    git \
    # Playwright dependencies
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Git configuration
RUN git config --global url."https://".insteadOf git:// && \
    git config --global url."https://".insteadOf ssh://git@

RUN mkdir -p /app

# 임시 디렉토리 생성 (import_export용)
RUN mkdir -p /app/tmp && chmod 777 /app/tmp

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM base AS builder

COPY pyproject.toml uv.lock /_lock/

RUN --mount=type=cache,target=/root/.cache \
  cd /_lock/ && \
  uv sync --frozen --no-install-project

# Install Playwright browsers (without cache mount to persist in image)
RUN /app/.venv/bin/playwright install --with-deps chromium

WORKDIR /app/webapp

COPY ./webapp /app/webapp

ENV PATH="/app/.venv/bin:$PATH"

COPY ./environments/production/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

EXPOSE ${PORT}
