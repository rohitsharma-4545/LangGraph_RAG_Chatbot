from app.core.celery_app import celery_app

# Force task registration
import app.tasks.ingestion_task