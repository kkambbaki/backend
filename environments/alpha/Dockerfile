FROM python:3.12-slim-trixie as python-base

ARG PORT=8000
ENV PORT=${PORT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# --- Builder Stage ---
FROM python-base AS builder

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Git configuration
RUN git config --global url."https://".insteadOf git:// && \
    git config --global url."https://".insteadOf ssh://git@

# Pin uv version for reproducible builds
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache \
  uv sync --frozen --no-install-project
COPY ./webapp /app/webapp

# --- Final Stage ---
FROM python-base

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a non-root user to run the application
RUN groupadd --system app && useradd --system --gid app appuser
# 임시 디렉토리 생성 (import_export용) - More secure permissions
RUN mkdir -p /app/tmp && chown -R appuser:app /app/tmp && chmod 755 /app/tmp

COPY --from=builder --chown=appuser:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=appuser:app ./environments/alpha/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser

ENTRYPOINT [ "/app/entrypoint.sh" ]

EXPOSE ${PORT}
