#!/bin/sh

sleep 7

alembic upgrade head

sleep 1

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

exec "$@"