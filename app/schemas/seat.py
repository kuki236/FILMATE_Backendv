"""Esquemas para asientos y bloqueo transaccional de butacas."""

from typing import List, Optional

from pydantic import BaseModel


class SeatBase(BaseModel):
    id_sala: int
    fila: str
    numero: int
    coord_x: Optional[int] = None
    coord_y: Optional[int] = None


class SeatCreate(SeatBase):
    pass


class SeatResponse(SeatBase):
    id_asiento: int
    estado_fisico: str

    class Config:
        from_attributes = True


class ShowtimeSeatItem(BaseModel):
    id_asiento: int
    fila: str
    numero: int
    estado: str


class SeatMapResponse(BaseModel):
    id_funcion: int
    id_sala: int
    asientos: List[ShowtimeSeatItem]


class SeatLockRequest(BaseModel):
    id_funcion: int
    ids_asientos: List[int]


class SeatLockResponse(BaseModel):
    id_funcion: int
    ids_asientos_bloqueados: List[int]
    estado: str