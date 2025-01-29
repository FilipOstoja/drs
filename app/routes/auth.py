from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db_connection
from app.crud import create_user, authenticate_user
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer za automatsko dohvaćanje tokena iz headera
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        role = payload.get("role")
        if user is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": user, "role": role}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/register")
async def register_user(username: str, email: str, password: str, db=Depends(get_db_connection)):
    hashed_password = pwd_context.hash(password)
    try:
        create_user(db, username, email, hashed_password)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(username: str, password: str, db=Depends(get_db_connection)):
    try:
        user = authenticate_user(db, username, password, pwd_context)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": username, "role": user["role"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Zaštićena ruta za admin pristup
@router.get("/admin-data")
async def get_admin_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You do not have access to this resource")
    return {"message": "This is protected data for admins only"}
