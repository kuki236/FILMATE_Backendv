from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.core.dependencies import get_db
from app.models.reservation import Reserva
from app.models.user import Usuario
from app.schemas.reservation import ReservationResponse

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("/user/{user_id}", response_model=List[ReservationResponse])
def list_user_reservations(user_id: int, db: Session = Depends(get_db)):
    user = db.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return (
        db.query(Reserva)
        .filter(Reserva.id_usuario == user_id)
        .order_by(Reserva.fecha_reserva.desc())
        .all()
    )


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = (
        db.query(Reserva)
        .options(
            joinedload(Reserva.boletos),
            joinedload(Reserva.snacks),
            joinedload(Reserva.funcion),
        )
        .filter(Reserva.id_reserva == reservation_id)
        .first()
    )
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
