"""Rutas de autenticación."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import LoginResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import authenticate_user, register_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, summary="Registrar un nuevo usuario")
def register(payload: UserCreate, db: Session = Depends(get_db)):
	"""Registra un usuario nuevo en la base de datos."""

	logger.info("📥 POST /auth/register - correo=%s", payload.correo)
	try:
		return register_user(db, payload)
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc))
	except Exception as exc:
		logger.error("❌ Error en POST /auth/register: %s", exc, exc_info=True)
		raise HTTPException(status_code=500, detail=str(exc))


@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión")
def login(payload: UserLogin, db: Session = Depends(get_db)):
	"""Valida credenciales y devuelve el usuario autenticado."""

	logger.info("📥 POST /auth/login - correo=%s", payload.correo)
	try:
		user = authenticate_user(db, payload)
		return LoginResponse(message="Login successful", user=user)
	except ValueError as exc:
		raise HTTPException(status_code=401, detail=str(exc))
	except Exception as exc:
		logger.error("❌ Error en POST /auth/login: %s", exc, exc_info=True)
		raise HTTPException(status_code=500, detail=str(exc))

