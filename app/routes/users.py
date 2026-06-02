from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models.user import Usuario
from app.core import security
from app.repositories import user_repository

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
def list_users(
    estado: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Usuario)
    if estado:
        query = query.filter(Usuario.estado == estado)
    return query.order_by(Usuario.fecha_registro.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = user_repository.get_user_by_email(db, payload.correo)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = security.hash_password(payload.password)
    user = Usuario(
        id_rol=2,
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        correo=payload.correo,
        password_hash=hashed
    )

    created = user_repository.create_user(db, user)
    return created


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.nombres is not None:
        user.nombres = payload.nombres
    if payload.apellidos is not None:
        user.apellidos = payload.apellidos
    if payload.correo is not None:
        existing = user_repository.get_user_by_email(db, payload.correo)
        if existing and existing.id_usuario != user_id:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.correo = payload.correo
    if payload.estado is not None:
        user.estado = payload.estado

    db.commit()
    db.refresh(user)
    return user
