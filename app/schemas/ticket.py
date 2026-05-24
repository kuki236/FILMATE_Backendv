"""Esquemas para boletos y payload QR final."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TicketBase(BaseModel):
    id_reserva: int
    id_funcion: int
    id_asiento: int
    id_tarifa: int
    precio_pagado: float


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id_boleto: int
    codigo_qr: str
    estado_ingreso: str

    class Config:
        from_attributes = True


class TicketIssueRequest(BaseModel):
    id_usuario: int
    id_funcion: int
    ids_asientos: List[int]
    id_tarifa: int
    id_promocion: Optional[int] = None
    metodo_pago: Optional[str] = None
    transaccion_id: Optional[str] = None
    fecha_expiracion: Optional[datetime] = None


class TicketQrPayload(BaseModel):
    version: str
    generado_en: datetime
    reserva: Dict[str, Any]
    boletos: List[Dict[str, Any]]
    payload_json: str


class TicketIssueResponse(BaseModel):
    reserva: Dict[str, Any]
    boletos: List[TicketResponse]
    qr: TicketQrPayload