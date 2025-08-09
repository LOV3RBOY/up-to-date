"""Celery application instance for asynchronous tasks.

This module exposes a Celery app configured to use the broker URL from
environment variables.  Tasks are discovered from the `backend/celery`
package when the worker starts.
"""

import os

from celery import Celery


def make_celery() -> Celery:
    """Create and configure the Celery application."""
    broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    backend_url = os.getenv("CELERY_RESULT_BACKEND", broker_url)
    app = Celery(
        "ebc_intel",
        broker=broker_url,
        backend=backend_url,
        include=["backend.celery.tasks"],
    )
    # Celery configuration
    app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone=os.getenv("TZ", "UTC"),
        enable_utc=True,
    )
    return app


celery_app = make_celery()
