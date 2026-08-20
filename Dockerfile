FROM python:3.12-alpine
LABEL authors="jackli"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY . .

RUN uv sync

ENTRYPOINT ["uv", "run" ,"uvicorn" ,"src.sunset_server:app", "--reload", "--port", "8190"]
