#!/usr/bin/env sh
set -e

# Apply database migrations before starting the API.
python -m alembic upgrade head

exec "$@"
