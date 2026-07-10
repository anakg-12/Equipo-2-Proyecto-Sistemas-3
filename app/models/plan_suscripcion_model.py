from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.bd.database import Base

class PlanSuscripcionModel(Base):
    __tablename__ = "plan_suscripcion"

    plan_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)
    duracion_dias = Column(Integer, nullable=False)
    costo = Column(Numeric(10,2), nullable=False)
    tipo = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True)

    membresias = relationship("MembresiaClienteModel", back_populates="plan")