from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class MotivoDevolucion(Base):
    __tablename__ = "motivo_devolucion"

    id_motivo = Column(Integer, primary_key=True)
    descripcion = Column(String(150), unique=True, nullable=False)

    solicitudes = relationship("SolicitudReembolso", back_populates="motivo")
