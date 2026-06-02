from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SolicitudReembolso(Base):
    __tablename__ = "solicitud_reembolso"

    id_solicitud = Column(Integer, primary_key=True)
    id_reserva = Column(Integer, ForeignKey("reserva.id_reserva"), nullable=False)
    id_motivo = Column(Integer, ForeignKey("motivo_devolucion.id_motivo"), nullable=False)
    id_administrador = Column(Integer, ForeignKey("usuario.id_usuario"))
    fecha_solicitud = Column(DateTime, nullable=False, server_default=func.now())
    monto_reembolsado = Column(DECIMAL(10, 2), nullable=False)
    tipo_reembolso = Column(
        Enum("Reembolso total", "Reembolso parcial", "Sin reembolso", name="tipo_reembolso"),
        nullable=False
    )
    estado_solicitud = Column(
        Enum("Pendiente", "Aprobada", "Rechazada", name="estado_solicitud"),
        default="Pendiente"
    )
    detalle_motivo = Column(Text)
    comentario_resolucion = Column(Text)
    fecha_resolucion = Column(DateTime)

    reserva = relationship("Reserva", back_populates="solicitudes")
    motivo = relationship("MotivoDevolucion", back_populates="solicitudes")
    administrador = relationship("Usuario", foreign_keys=[id_administrador])
