from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SolicitudReembolsoBase(BaseModel):
    id_reserva: int
    id_motivo: int
    monto_reembolsado: float
    tipo_reembolso: str
    detalle_motivo: Optional[str] = None


class SolicitudReembolsoCreate(SolicitudReembolsoBase):
    pass


class SolicitudReembolsoUpdate(BaseModel):
    id_administrador: Optional[int] = None
    estado_solicitud: Optional[str] = None
    comentario_resolucion: Optional[str] = None
    fecha_resolucion: Optional[datetime] = None


class SolicitudReembolsoResponse(SolicitudReembolsoBase):
    id_solicitud: int
    id_administrador: Optional[int] = None
    fecha_solicitud: datetime
    estado_solicitud: str
    comentario_resolucion: Optional[str] = None
    fecha_resolucion: Optional[datetime] = None

    class Config:
        from_attributes = True
