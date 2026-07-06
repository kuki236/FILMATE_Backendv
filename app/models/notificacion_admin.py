from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, text
from app.core.database import Base


class NotificacionAdmin(Base):
    __tablename__ = "notificaciones_admin"

    id_notificacion = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(30), nullable=False)
    titulo = Column(String(100), nullable=False)
    mensaje = Column(Text, nullable=False)
    modulo = Column(String(50), nullable=False)
    leida = Column(Boolean, default=False)
    id_usuario_destino = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
