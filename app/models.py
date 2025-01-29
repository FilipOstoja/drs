from pydantic import BaseModel
from typing import Optional

class DocumentCreate(BaseModel):
    filename: str
    filetype: str
    size: int
    owner_id: int

class DocumentResponse(BaseModel):
    id: int
    filename: str
    filetype: str
    size: int
    owner_id: int

    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    username: str
    email: str
    password: str