FROM python:3.14-slim

# uv, pinned, straight from its official image
COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /usr/local/bin/uv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependencies first: this layer is rebuilt only when pyproject.toml or uv.lock change.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

# The app: the Python code and the files the browser loads (src/paths.py finds static/ next to src/).
COPY src ./src
COPY static ./static
ENV PATH="/app/.venv/bin:$PATH"

RUN useradd --system --home-dir /app app
USER app

EXPOSE 8080
CMD ["uvicorn", "server:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8080"]
