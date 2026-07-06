import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_superadmin
from app.models.log_actividad_sistema import LogActividadSistema
from app.repositories import role_repository
from app.schemas.permiso import PermisoResponse
from app.schemas.rol import RolCreate, RolResponse, RolUpdate, RolWithPermisosResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/roles", tags=["admin roles"])


@router.get("/", response_model=List[RolResponse])
def list_roles(
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    return role_repository.list_roles(db)


@router.post("/", response_model=RolResponse, status_code=201)
def create_role(
    request: Request,
    payload: RolCreate,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    existing = role_repository.get_role_by_id(db, 0)
    try:
        rol = role_repository.create_role(db, payload.nombre_rol, payload.descripcion)
        db.add(LogActividadSistema(
            id_usuario=_superadmin.get("user_id"),
            accion_realizada=f"Rol creado: {rol.nombre_rol}",
            modulo_afectado="ROLES",
            ip_origen=request.client.host if request.client else "0.0.0.0",
        ))
        db.commit()
        return rol
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{role_id}", response_model=RolWithPermisosResponse)
def get_role(
    role_id: int,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    result = role_repository.get_role_with_permisos(db, role_id)
    if not result:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return result


@router.put("/{role_id}", response_model=RolResponse)
def update_role(
    request: Request,
    role_id: int,
    payload: RolUpdate,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    data = payload.model_dump(exclude_unset=True)
    rol = role_repository.update_role(db, role_id, data)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Rol editado: {role_id}",
        modulo_afectado="ROLES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return rol


@router.delete("/{role_id}")
def delete_role(
    request: Request,
    role_id: int,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    if not role_repository.delete_role(db, role_id):
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Rol eliminado: {role_id}",
        modulo_afectado="ROLES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": "Rol eliminado correctamente"}


@router.get("/{role_id}/permisos", response_model=List[PermisoResponse])
def get_role_permisos(
    role_id: int,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    permisos = role_repository.get_role_permisos(db, role_id)
    return [PermisoResponse.model_validate(p) for p in permisos]


@router.put("/{role_id}/permisos", response_model=List[PermisoResponse])
def set_role_permisos(
    request: Request,
    role_id: int,
    payload: List[int],
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    role_repository.assign_permisos_to_role(db, role_id, payload)
    permisos = role_repository.get_role_permisos(db, role_id)
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Permisos asignados a rol {role_id}",
        modulo_afectado="ROLES",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return [PermisoResponse.model_validate(p) for p in permisos]
