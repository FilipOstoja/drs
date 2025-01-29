from fastapi import FastAPI
from app.database import get_db_connection, close_db_connection
from app.routes import documents
from app.routes.auth import router as auth_router




app = FastAPI()

@app.get("/test-db-connection")
def test_db_connection():
    connection = get_db_connection()
    if connection:
        close_db_connection(connection)
        return {"status": "success", "message": "Database connected"}
    else:
        return {"status": "error", "message": "Failed to connect to database"}
    
app.include_router(documents.router)
app.include_router(auth_router)


