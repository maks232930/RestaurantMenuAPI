#!/bin/sh

./wait-for-it.sh db:5432 --timeout=60
./wait-for-it.sh redis:6379 --timeout=60

alembic upgrade head

sleep 1

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

exec "$@"