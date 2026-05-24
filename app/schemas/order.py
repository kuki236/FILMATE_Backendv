"""Esquemas para el cierre de compra y confirmación de reserva."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.ticket import TicketResponse, TicketQrPayload


class SnackOrderItem(BaseModel):
	id_producto: int
	cantidad: int


class CheckoutRequest(BaseModel):
	id_usuario: int
	id_funcion: int
	ids_asientos: List[int]
	id_tarifa: int
	id_promocion: Optional[int] = None
	metodo_pago: Optional[str] = None
	transaccion_id: Optional[str] = None
	snacks: List[SnackOrderItem] = Field(default_factory=list)
	fecha_expiracion: Optional[datetime] = None


class CheckoutResponse(BaseModel):
	id_reserva: int
	estado_pago: str
	monto_subtotal: float
	descuento_aplicado: float
	monto_total: float
	boletos: List[TicketResponse]
	qr: TicketQrPayload
