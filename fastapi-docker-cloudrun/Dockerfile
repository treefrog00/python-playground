FROM python:3.13.2-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /uvx /bin/

# StreamHandler in CPython already flushes after each emit/line, not entirely sure if this is really necessary
ENV PYTHONUNBUFFERED=1
ENV PORT=1234

WORKDIR /app
ADD . /app
RUN uv sync --frozen

# As an example here we're running the web service with one worker on uvicorn.
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}", "--workers", "1"]