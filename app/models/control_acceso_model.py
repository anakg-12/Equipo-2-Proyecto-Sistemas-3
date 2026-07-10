from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.bd.database import Base

class ControlAccesoModel(Base):
    __tablename__ = "control_acceso"

    acceso_id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)
    fecha_hora_entrada = Column(DateTime, server_default=func.now())
    validado = Column(Boolean, default=True)
    observaciones = Column(Text)

    cliente = relationship("ClienteModel", back_populates="accesos")