# Before starting celery start redis

myenv\Scripts\activate

uvicorn app.main:app --reload

docker run -d -p 6379:6379 redis

celery -A app.worker.celery_worker worker --loglevel=info --pool=solo

---

Chatbot\app\core\celery_app.py

# add this celery for ingestion

celery_app.conf.task_routes = {
"app.tasks.ingestion_task.process_pdf": {"queue": "ingestion"}
}

# use this in terminal if you are adding ingestion

celery -A app.worker.celery_worker worker --loglevel=info --pool=solo -Q ingestion
