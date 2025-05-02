"""Module for Celery worker configuration."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
)

celery_app.autodiscover_tasks(["app.tasks"])
