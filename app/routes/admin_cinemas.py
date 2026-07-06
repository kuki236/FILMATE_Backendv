import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_permiso
from app.models.cinema import Cine
from app.models.log_actividad_sistema import LogActividadSistema
from app.schemas.cinema import CinemaCreate, CinemaResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/cinemas", tags=["admin cinemas"])


@router.get("/", response_model=List[CinemaResponse])
def admin_list_cinemas(
    db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_CINES"))],
):
    return db.query(Cine).filter(Cine.eliminado == False).all()


@router.post("/", response_model=CinemaResponse, status_code=201)
def create_cinema(
    request: Request,
    payload: CinemaCreate,
    db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_CINES"))],
):
    cine = Cine(**payload.model_dump())
    db.add(cine)
    db.commit()
    db.refresh(cine)
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Cine creado: {cine.nombre_cine}",
        modulo_afectado="CINES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return cine


@router.put("/{cinema_id}", response_model=CinemaResponse, responses={404: {"description": "Cine no encontrado"}})
def update_cinema(
    request: Request,
    cinema_id: int, payload: CinemaCreate, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_CINES"))],
):
    cine = db.query(Cine).filter(Cine.id_cine == cinema_id, Cine.eliminado == False).first()
    if not cine:
        raise HTTPException(status_code=404, detail="Cine no encontrado")
    for key, value in payload.model_dump().items():
        setattr(cine, key, value)
    db.commit()
    db.refresh(cine)
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Cine editado: {cinema_id}",
        modulo_afectado="CINES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return cine


@router.delete("/{cinema_id}", responses={404: {"description": "Cine no encontrado"}})
def delete_cinema(
    request: Request,
    cinema_id: int, db: Annotated[Session, Depends(get_db)],
    _permiso: Annotated[dict, Depends(require_permiso("GESTIONAR_CINES"))],
):
    from datetime import datetime
    cine = db.query(Cine).filter(Cine.id_cine == cinema_id, Cine.eliminado == False).first()
    if not cine:
        raise HTTPException(status_code=404, detail="Cine no encontrado")
    cine.eliminado = True
    cine.fecha_eliminacion = datetime.now()
    db.commit()
    db.add(LogActividadSistema(
        id_usuario=_permiso.get("user_id"),
        accion_realizada=f"Cine eliminado: {cinema_id}",
        modulo_afectado="CINES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": "Cine desactivado"}
