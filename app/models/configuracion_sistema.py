from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from app.core.database import Base


class ConfiguracionSistema(Base):
    __tablename__ = "configuracion_sistema"

    id_config = Column(Integer, primary_key=True)
    clave = Column(String(100), nullable=False, unique=True)
    valor = Column(Text, nullable=False)
    descripcion = Column(String(255))
    tipo_dato = Column(String(20), nullable=False, default='string')
    categoria = Column(String(50), nullable=False, default='general')
    activo = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
