from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionItem(BaseModel):
    id_reserva: int
    cliente: str
    pelicula: str
    sala: str

    monto_total: float

    estado_pago: str
    metodo_pago: Optional[str] = None

    fecha_compra: Optional[datetime] = None

    class Config:
        from_attributes = True


class TransactionDetail(BaseModel):
    id_reserva: int

    cliente: str
    correo: str

    pelicula: str
    sala: str

    monto_subtotal: float
    descuento_aplicado: float
    monto_total: float

    estado_pago: str
    metodo_pago: Optional[str] = None
    transaccion_id: Optional[str] = None

    class Config:
        from_attributes = True