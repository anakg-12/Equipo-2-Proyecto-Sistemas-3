from sqlalchemy import Column, Integer, String, Date, Text, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.bd.database import Base

class EvaluacionBiometricaModel(Base):
    __tablename__ = "evaluacion_biometrica"

    evaluacion_id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id", ondelete="CASCADE"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("entrenador.entrenador_id", ondelete="SET NULL"), nullable=False)
    fecha = Column(Date, server_default=func.current_date())
    peso = Column(Numeric(5,2))
    estatura = Column(Numeric(5,2))
    porcentaje_grasa = Column(Numeric(5,2))
    observaciones = Column(Text)

    cliente_evaluado = relationship("ClienteModel", back_populates="evaluaciones")
    entrenador_asignado = relationship("EntrenadorModel", foreign_keys=[entrenador_id], back_populates="evaluaciones")