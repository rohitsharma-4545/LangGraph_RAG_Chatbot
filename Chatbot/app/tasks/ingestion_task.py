from app.core.celery_app import celery_app 

from app.core.document_loader import load_pdf
from app.core.text_splitter import split_docs
from app.services.vector_store import add_documents


@celery_app.task(name="app.tasks.ingestion_task.process_pdf")
def process_pdf(file_path: str):
    try:
        print("🔥 Processing started")

        docs = load_pdf(file_path)
        print("Docs loaded:", len(docs))

        chunks = split_docs(docs)
        print("Chunks created:", len(chunks))

        add_documents(chunks)

        print("✅ Stored in vector DB")

        return {"status": "completed", "chunks": len(chunks)}

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise e