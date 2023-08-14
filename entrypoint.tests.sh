#!/bin/sh

./wait-for-it.sh db_test:5432 --timeout=60
./wait-for-it.sh redis_test:6379 --timeout=60
./wait-for-it.sh rabbitmq:5672 --timeout=60

sleep 5

alembic upgrade head

sleep 1

uvicorn src.main:app --host 0.0.0.0 --port 8888 --reload

exec "$@"
