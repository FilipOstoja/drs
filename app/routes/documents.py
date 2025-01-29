import os
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from app.database import get_db_connection
from app.routes.auth import get_current_user
from app.services.email_service import send_email

# Inicijalizacija loggera
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Provjera postoji li direktorij za pohranu datoteka, ako ne, stvaranje
if not os.path.exists('files'):
    os.makedirs('files')

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    connection = get_db_connection()
    try:
        logger.info(f"Started file upload process for: {file.filename}")

        # Određivanje putanje gdje će se datoteka spremiti
        file_location = f"files/{file.filename}"
        logger.info(f"File will be saved to: {file_location}")

        # Spremanje datoteke na disk
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"File {file.filename} has been saved to disk")

        # Dohvati tip datoteke i veličinu
        filetype = file.content_type  # MIME tip datoteke (npr. "application/pdf")
        size = len(content)  # Veličina u bajtovima

        # Spremanje informacija u bazu podataka
        if connection:
            cursor = connection.cursor()
            query = """INSERT INTO documents (filename, file_path, filetype, size, owner_username) 
                       VALUES (%s, %s, %s, %s, %s)"""
            
            # Logiranje izvršenja SQL upita
            logger.info(f"Executing query: {query} with values ({file.filename}, {file_location}, {filetype}, {size}, {current_user['username']})")
            
            cursor.execute(query, (file.filename, file_location, filetype, size, current_user["username"]))
            connection.commit()

            # Logiranje uspješnog unosa u bazu
            logger.info(f"Document {file.filename} saved to database with owner username {current_user['username']}")

            return {"message": f"File '{file.filename}' uploaded and saved in the database!"}
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to database")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": str(e)}

    finally:
        if connection:
            connection.close()

@router.get("/documents")
async def get_documents(current_user: dict = Depends(get_current_user)):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)

        # Ako je admin, dohvaća sve dokumente
        if current_user["role"] == "admin":
            query = "SELECT id, filename, file_path, filetype, size, owner_username, created_at FROM documents"
            params = []
        else:
            # Ako nije admin, dohvaća samo svoje dokumente
            query = "SELECT id, filename, file_path, filetype, size, owner_username, created_at FROM documents WHERE owner_username = %s"
            params = [current_user["username"]]

        logger.info(f"Executing query: {query} with params {params}")
        cursor.execute(query, params)
        documents = cursor.fetchall()

        return {"documents": documents}

    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        if connection:
            connection.close()


@router.post("/documents/forward/{document_id}")
async def forward_document(
    document_id: int,
    recipient_email: str = Form(...),  # Koristi Form za dohvat podataka iz tijela zahtjeva
    current_user: dict = Depends(get_current_user)
):
    connection = get_db_connection()
    try:
        # Provjera je li korisnik admin
        if current_user["role"] != "admin":
            raise HTTPException(status_code=403, detail="You do not have access to this resource")

        # Dohvat dokumenta iz baze prema ID-u
        cursor = connection.cursor()
        query = "SELECT filename, file_path FROM documents WHERE id = %s"
        cursor.execute(query, (document_id,))
        document = cursor.fetchone()

        if document:
            filename, file_path = document
            # Slanje e-maila sa dokumentom
            subject = f"Forwarded Document: {filename}"
            body = f"Please find the document {filename} attached."
            send_email(recipient_email, subject, body, file_path)  # Dodano file_path za privitak

            logger.info(f"Document {filename} forwarded to {recipient_email}")
            return {"message": f"Document '{filename}' successfully forwarded to {recipient_email}!"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")

    except Exception as e:
        # Logiranje pogreške ako dođe do izuzetka
        logger.error(f"Error: {str(e)}")
        return {"error": str(e)}

    finally:
        if connection:
            connection.close()