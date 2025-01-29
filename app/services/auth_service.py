import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret"

async def login(username: str, password: str):
    # Dummy korisnik
    if username == "admin" and password == "password":
        token = jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY)
        return {"access_token": token}
    return {"error": "Invalid credentials"}

async def register(username: str, password: str):
    return {"message": f"User {username} registered successfully"}
