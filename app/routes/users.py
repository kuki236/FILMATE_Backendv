from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import Usuario
from app.core import security
from app.repositories import user_repository

router = APIRouter(prefix="/users", tags=["users"])


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
