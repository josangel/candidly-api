"""Module for Celery worker configuration."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "candidly_tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "default"},
}

celery_app.conf.accept_content = ["json"]
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
