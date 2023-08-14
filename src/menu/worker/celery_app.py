from celery import Celery

from src.config import (
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
)

celery_app = Celery('RestaurantMenuApi',
                    broker=f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}',
                    include=['src.menu.worker.tasks.excel_sync_task'])

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Minsk',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'sync_excel_to_db': {
        'task': 'src.menu.worker.tasks.excel_sync_task.sync_excel_to_db',
        'schedule': 15.0,
    },
}
