from sqlalchemy.orm import Session
from app.models.user import Usuario
from typing import Optional


def get_user_by_id(db: Session, user_id: int) -> Optional[Usuario]:
	return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
	return db.query(Usuario).filter(Usuario.correo == email).first()


def create_user(db: Session, user: Usuario) -> Usuario:
	db.add(user)
	db.commit()
	db.refresh(user)
	return user
