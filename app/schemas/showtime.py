"""Esquemas para funciones, horarios y disponibilidad por sede."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ShowtimeBase(BaseModel):
    id_pelicula: int
    id_sala: int
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    idioma: Optional[str] = None
    formato: Optional[str] = None


class ShowtimeCreate(ShowtimeBase):
    pass


class ShowtimeResponse(ShowtimeBase):
    id_funcion: int

    class Config:
        from_attributes = True


class SeatAvailabilityItem(BaseModel):
    id_asiento: int
    fila: str
    numero: int
    estado: str


class ShowtimeAvailabilityItem(BaseModel):
    id_funcion: int
    id_pelicula: int
    titulo_pelicula: str
    id_sala: int
    nombre_sala: str
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    idioma: Optional[str] = None
    formato: Optional[str] = None
    asientos_totales: int
    asientos_disponibles: int


class CinemaShowtimesResponse(BaseModel):
    id_cine: int
    nombre_cine: str
    ciudad: Optional[str] = None
    funciones: List[ShowtimeAvailabilityItem]


class ShowtimeUpdate(ShowtimeBase):
    pass