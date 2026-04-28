from fastapi import APIRouter, UploadFile, Depends
import os

from app.tasks.ingestion_task import process_pdf
from app.auth.dependencies import require_admin
from app.services.vector_store import clear_collection
from app.auth.dependencies import require_admin

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(
    file: UploadFile,
    user=Depends(require_admin)
):
    clear_collection()

    delete_existing_files()

    file_path = os.path.abspath(f"{UPLOAD_DIR}/{file.filename}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    task = process_pdf.delay(file_path)

    return {
        "message": "Old data cleared. New PDF processing started.",
        "task_id": task.id
    }

@router.delete("/delete")
def delete_pdf(user=Depends(require_admin)):
    clear_collection()
    delete_existing_files()

    return {"message": "All documents deleted"}

def delete_existing_files():
    for file in os.listdir(UPLOAD_DIR):
        os.remove(os.path.join(UPLOAD_DIR, file))