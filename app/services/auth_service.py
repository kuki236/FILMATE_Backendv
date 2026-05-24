"""Servicios de autenticación y registro de usuarios."""

from sqlalchemy.orm import Session

from app.core import security
from app.models.user import Usuario
from app.repositories import user_repository
from app.schemas.user import UserCreate, UserLogin


def register_user(db: Session, payload: UserCreate, default_role_id: int = 2) -> Usuario:
	"""Crea un usuario nuevo en la base de datos.

	Valida que el correo no exista, cifra la contraseña y guarda el registro
	con el rol por defecto para usuarios finales.
	"""

	existing = user_repository.get_user_by_email(db, payload.correo)
	if existing:
		raise ValueError("Email already registered")

	hashed_password = security.hash_password(payload.password)
	user = Usuario(
		id_rol=default_role_id,
		nombres=payload.nombres,
		apellidos=payload.apellidos,
		correo=payload.correo,
		password_hash=hashed_password,
	)

	return user_repository.create_user(db, user)


def authenticate_user(db: Session, payload: UserLogin) -> Usuario:
	"""Valida credenciales y devuelve el usuario autenticado.

	El usuario debe existir, la contraseña debe coincidir y la cuenta debe
	estar en estado `Activo`.
	"""

	user = user_repository.get_user_by_email(db, payload.correo)
	if not user:
		raise ValueError("Invalid credentials")

	if not security.verify_password(payload.password, user.password_hash):
		raise ValueError("Invalid credentials")

	if user.estado != "Activo":
		raise ValueError("User account is not active")

	return user

