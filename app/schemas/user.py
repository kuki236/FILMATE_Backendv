from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[str] = None


class UserLogin(BaseModel):
    correo: EmailStr
    password: str


class UserResponse(UserBase):
    id_usuario: int
    id_rol: int
    estado: str
    fecha_registro: datetime

    class Config:
        from_attributes = True
