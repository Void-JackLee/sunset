FROM python:3.12-alpine
LABEL authors="jackli"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

COPY . .

ENTRYPOINT ["uv", "run", "--no-dev", "uvicorn" ,"src.sunset_server:app", "--host", "0.0.0.0", "--port", "8190"]
