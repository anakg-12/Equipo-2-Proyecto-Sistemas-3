from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.bd.database import Base

class ReservaInscripcionModel(Base):
    __tablename__ = "reserva_inscripcion"

    reserva_id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)
    sesion_id = Column(Integer, ForeignKey("sesion_programada.sesion_id"), nullable=False)
    fecha_reserva = Column(DateTime, server_default=func.now())
    estado = Column(String(20), nullable=False, default="activa")

    cliente = relationship("ClienteModel", back_populates="reservas")
    sesion = relationship("SesionProgramadaModel", back_populates="reservas")