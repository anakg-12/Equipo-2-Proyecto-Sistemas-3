from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.bd.database import Base
from app.constants import TicketState

class TicketMantenimientoModel(Base):
    __tablename__ = "ticket_mantenimiento"

    ticket_id = Column(Integer, primary_key=True)
    maquina_id = Column(Integer, ForeignKey("maquina.maquina_id"), nullable=False)
    fecha_reporte = Column(DateTime, server_default=func.now())
    descripcion_falla = Column(Text, nullable=False)
    fecha_resolucion = Column(DateTime, nullable=True)
    costo_reparacion = Column(Numeric(10,2), nullable=True)
    estado = Column(String(20), nullable=False, default=TicketState.abierto.value)
    reportado_por = Column(Integer, ForeignKey("usuario.usuario_id"), nullable=False)

    maquina = relationship("MaquinaModel", back_populates="tickets")
    reportado_por_usuario = relationship("UsuarioModel", foreign_keys=[reportado_por])