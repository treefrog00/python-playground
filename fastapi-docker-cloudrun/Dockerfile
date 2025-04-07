FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /uvx /bin/

# StreamHandler in CPython already flushes after each emit/line, not entirely sure if this is really necessary
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# As an example here we're running the web service with one worker on uvicorn.
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]