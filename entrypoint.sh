#!/usr/bin/env sh
set -e

# Apply database migrations before starting the API.
uv run alembic upgrade head

exec "$@"
