from celery import Celery

from app.config import setting

broker_connection_retry_on_startup = True
celery = Celery(
    "tasks",
    broker=f"redis://{setting.REDIS_HOST}:{setting.REDIS_PORT}",
    include=["app.tasks.tasks"]
)