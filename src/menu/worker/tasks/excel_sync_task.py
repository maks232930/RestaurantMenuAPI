from src.menu.worker.celery_app import celery_app


@celery_app.task
def sync_excel_to_db():
    print(10)
    pass
