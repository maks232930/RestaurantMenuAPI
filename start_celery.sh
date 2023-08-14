#!/bin/bash

./wait-for-it.sh rabbitmq:5672 --timeout=100

sleep 5

celery -A src.menu.worker.celery_app worker &

sleep 15

celery -A src.menu.worker.celery_app beat
