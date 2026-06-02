from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.schemas.solicitud_reembolso import (
    SolicitudReembolsoCreate,
    SolicitudReembolsoResponse,
)
from app.schemas.motivo_devolucion import MotivoDevolucionResponse
from app.repositories import reembolso_repository

router = APIRouter(
    prefix="/api/reembolsos",
    tags=["reembolsos"]
)


@router.get("/motivos", response_model=List[MotivoDevolucionResponse])
def list_motivos(db: Session = Depends(get_db)):
    return reembolso_repository.list_motivos(db)


@router.post("/", response_model=SolicitudReembolsoResponse, status_code=201)
def create_solicitud(
    payload: SolicitudReembolsoCreate,
    db: Session = Depends(get_db),
):
    return reembolso_repository.create_solicitud(
        db=db,
        id_reserva=payload.id_reserva,
        id_motivo=payload.id_motivo,
        monto_reembolsado=payload.monto_reembolsado,
        tipo_reembolso=payload.tipo_reembolso,
        detalle_motivo=payload.detalle_motivo,
    )


@router.get("/mis-solicitudes", response_model=List[SolicitudReembolsoResponse])
def list_mis_solicitudes(
    id_usuario: int,
    db: Session = Depends(get_db),
):
    return reembolso_repository.list_solicitudes_by_user(db, id_usuario)
