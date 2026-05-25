"""Esquemas para salas de cine."""

from pydantic import BaseModel
from typing import Optional


class RoomBase(BaseModel):
    id_cine: int
    nombre: str
    formato_sala: Optional[str] = None
    capacidad_total: int


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    nombre: Optional[str] = None
    formato_sala: Optional[str] = None
    capacidad_total: Optional[int] = None


class RoomResponse(RoomBase):
    id_sala: int

    class Config:
        from_attributes = True