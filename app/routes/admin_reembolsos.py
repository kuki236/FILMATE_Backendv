from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.dependencies import get_db
from app.schemas.solicitud_reembolso import (
    SolicitudReembolsoResponse,
    SolicitudReembolsoUpdate,
)
from app.schemas.motivo_devolucion import (
    MotivoDevolucionCreate,
    MotivoDevolucionResponse,
)
from app.repositories import reembolso_repository

router = APIRouter(
    prefix="/api/admin/reembolsos",
    tags=["admin reembolsos"]
)


@router.get("/", response_model=List[SolicitudReembolsoResponse])
def list_solicitudes(
    estado: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    return reembolso_repository.list_solicitudes_admin(
        db, estado=estado, skip=skip, limit=limit
    )


@router.get("/metricas")
def get_metricas(db: Session = Depends(get_db)):
    return reembolso_repository.count_solicitudes_by_estado(db)


@router.get("/{solicitud_id}", response_model=SolicitudReembolsoResponse)
def get_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = reembolso_repository.get_solicitud(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud not found")
    return solicitud


@router.put("/{solicitud_id}", response_model=SolicitudReembolsoResponse)
def resolve_solicitud(
    solicitud_id: int,
    payload: SolicitudReembolsoUpdate,
    db: Session = Depends(get_db),
):
    solicitud = reembolso_repository.resolve_solicitud(
        db=db,
        solicitud_id=solicitud_id,
        id_administrador=payload.id_administrador,
        estado_solicitud=payload.estado_solicitud,
        comentario_resolucion=payload.comentario_resolucion,
    )
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud not found")
    return solicitud


# =========================================
# MOTIVOS (admin CRUD)
# =========================================

@router.post("/motivos", response_model=MotivoDevolucionResponse, status_code=201)
def create_motivo(payload: MotivoDevolucionCreate, db: Session = Depends(get_db)):
    return reembolso_repository.create_motivo(db, payload.descripcion)


@router.put("/motivos/{motivo_id}", response_model=MotivoDevolucionResponse)
def update_motivo(motivo_id: int, payload: MotivoDevolucionCreate, db: Session = Depends(get_db)):
    motivo = reembolso_repository.update_motivo(db, motivo_id, payload.descripcion)
    if not motivo:
        raise HTTPException(status_code=404, detail="Motivo not found")
    return motivo


@router.delete("/motivos/{motivo_id}")
def delete_motivo(motivo_id: int, db: Session = Depends(get_db)):
    deleted = reembolso_repository.delete_motivo(db, motivo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Motivo not found")
    return {"message": "Motivo deleted successfully"}
