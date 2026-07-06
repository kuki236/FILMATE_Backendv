import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_superadmin
from app.models.log_actividad_sistema import LogActividadSistema
from app.repositories import permission_repository
from app.schemas.permiso import PermisoCreate, PermisoResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/permisos", tags=["admin permisos"])


@router.get("/", response_model=List[PermisoResponse])
def list_permisos(
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    return permission_repository.list_permisos(db)


@router.post("/", response_model=PermisoResponse, status_code=201)
def create_permiso(
    request: Request,
    payload: PermisoCreate,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    try:
        permiso = permission_repository.create_permiso(
            db, payload.codigo_permiso, payload.descripcion, payload.modulo
        )
        db.add(LogActividadSistema(
            id_usuario=_superadmin.get("user_id"),
            accion_realizada=f"Permiso creado: {permiso.codigo_permiso}",
            modulo_afectado="PERMISOS",
            ip_origen=request.client.host if request.client else "0.0.0.0",
        ))
        db.commit()
        return permiso
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{permiso_id}")
def delete_permiso(
    request: Request,
    permiso_id: int,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    if not permission_repository.delete_permiso(db, permiso_id):
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Permiso eliminado: {permiso_id}",
        modulo_afectado="PERMISOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": "Permiso eliminado correctamente"}
