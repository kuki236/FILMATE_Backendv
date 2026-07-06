from datetime import datetime
from pydantic import BaseModel


class NotificacionOut(BaseModel):
    id_notificacion: int
    tipo: str
    titulo: str
    mensaje: str
    modulo: str
    leida: bool
    id_usuario_destino: int | None
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


class NotificacionListResponse(BaseModel):
    data: list[NotificacionOut]
    total: int
    page: int
    limit: int


class NotificacionCountResponse(BaseModel):
    count: int
