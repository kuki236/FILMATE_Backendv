from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.core.dependencies import get_db
from app.models.reservation import Reserva
from app.schemas.reservation import ReservationResponse

router = APIRouter(prefix="/api/admin/reservas", tags=["admin reservas"])


@router.get("/", response_model=List[ReservationResponse])
def list_all_reservations(
    estado: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Reserva).options(
        joinedload(Reserva.usuario),
        joinedload(Reserva.funcion),
        joinedload(Reserva.boletos),
    )
    if estado:
        query = query.filter(Reserva.estado_pago == estado)
    skip = (page - 1) * limit
    return query.order_by(Reserva.fecha_reserva.desc()).offset(skip).limit(limit).all()
