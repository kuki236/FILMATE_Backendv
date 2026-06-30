from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HistorialActividadResponse(BaseModel):
    id_actividad: int
    id_usuario: int
    username: Optional[str] = None
    url_perfil: Optional[str] = None
    tipo_evento: str
    id_referencia_usuario: Optional[int] = None
    referencia_username: Optional[str] = None
    id_referencia_pelicula: Optional[int] = None
    referencia_pelicula_titulo: Optional[str] = None
    id_referencia_resena: Optional[int] = None
    texto_breve: Optional[str] = None
    fecha_evento: Optional[datetime] = None

    model_config = {"from_attributes": True}
