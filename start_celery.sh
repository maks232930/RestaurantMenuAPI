#!/bin/bash

sleep 20

celery -A src.menu.worker.celery_app worker --loglevel=info &

sleep 15

celery -A src.menu.worker.celery_app beat --loglevel=info
