# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ src/
COPY data/ data/
RUN uv sync --frozen --no-dev

RUN uv pip install en_core_web_lg@https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser -m appuser

COPY --from=builder /app /app

RUN mkdir -p /app/models && chown -R appuser:appuser /app/models

ENV PATH="/app/.venv/bin:$PATH"
ENV R2J_ENVIRONMENT=prod

USER appuser

EXPOSE 8000

CMD ["uvicorn", "resume2job.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
