from fastapi import UploadFile
import shutil
import os

UPLOAD_FOLDER = "app/uploaded_files/"

async def save_document(file: UploadFile):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "saved"}

async def send_document_email(document_id: int, email: str):
    # Ova funkcija treba koristiti app.email_service
    return {"document_id": document_id, "sent_to": email}
