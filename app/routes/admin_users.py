import logging
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_superadmin
from app.models.log_actividad_sistema import LogActividadSistema
from app.repositories import user_repository
from app.schemas.user import (
    UserCreateAdmin, UserResponse, UserStatusUpdate,
    UserRoleAssignRequest, UserUpdate, PasswordUpdate,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/users", tags=["admin users"])


def _build_user_response(db: Session, user) -> UserResponse:
    r = UserResponse.model_validate(user)
    r.roles = user_repository.get_user_roles(db, user.id_usuario)
    return r


@router.get("/", response_model=List[UserResponse])
def admin_list_users(
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
    estado: Optional[str] = None,
):
    users = user_repository.list_users(db, estado)
    return [_build_user_response(db, u) for u in users]


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    request: Request,
    payload: UserCreateAdmin,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    from app.services.auth_service import register_user

    try:
        user = register_user(db, payload)
        if payload.role_ids:
            user_repository.set_user_roles(db, user.id_usuario, payload.role_ids)
        db.add(LogActividadSistema(
            id_usuario=_superadmin.get("user_id"),
            accion_realizada=f"Usuario creado: {user.nombre}",
            modulo_afectado="USUARIOS",
            ip_origen=request.client.host if request.client else "0.0.0.0",
        ))
        db.commit()
        return _build_user_response(db, user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    request: Request,
    user_id: int,
    payload: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    data = payload.model_dump(exclude_unset=True)
    user = user_repository.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Usuario editado: {user_id}",
        modulo_afectado="USUARIOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return _build_user_response(db, user)


@router.put("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    request: Request,
    user_id: int,
    payload: UserStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    user = user_repository.update_user(db, user_id, {"estado_usuario": payload.estado_usuario})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Estado cambiado a {payload.estado_usuario} - user {user_id}",
        modulo_afectado="USUARIOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return _build_user_response(db, user)


@router.delete("/{user_id}")
def delete_user(
    request: Request,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    user = user_repository.soft_delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Usuario eliminado: {user_id}",
        modulo_afectado="USUARIOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": "Usuario eliminado correctamente"}


@router.get("/{user_id}/roles", response_model=List[int])
def get_user_roles(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user_repository.get_user_roles(db, user_id)


@router.put("/{user_id}/roles", response_model=List[int])
def set_user_roles(
    request: Request,
    user_id: int,
    payload: UserRoleAssignRequest,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_repository.set_user_roles(db, user_id, payload.role_ids)
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Roles asignados a user {user_id}: {payload.role_ids}",
        modulo_afectado="USUARIOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return user_repository.get_user_roles(db, user_id)


@router.put("/{user_id}/password", response_model=dict)
def update_user_password(
    request: Request,
    user_id: int,
    payload: PasswordUpdate,
    db: Annotated[Session, Depends(get_db)],
    _superadmin: Annotated[dict, Depends(get_current_superadmin)],
):
    from app.core.security import hash_password
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.contrasena = hash_password(payload.contrasena)
    db.add(LogActividadSistema(
        id_usuario=_superadmin.get("user_id"),
        accion_realizada=f"Contraseña reseteada: user {user_id}",
        modulo_afectado="USUARIOS",
        ip_origen=request.client.host if request.client else "0.0.0.0",
    ))
    db.commit()
    return {"message": "Contraseña actualizada correctamente"}
