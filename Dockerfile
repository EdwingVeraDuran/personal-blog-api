## -------------------------------- Builder Stage ------------------------------- ##
FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends -y build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY ./pyproject.toml .
COPY ./uv.lock .

RUN uv sync --locked

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

## -------------------------------- Production Stage ------------------------------- ##
FROM python:3.12-slim-bookworm AS production

WORKDIR /app

COPY /src src
COPY --from=builder /app/.venv/ .venv

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
