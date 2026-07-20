from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.bd.database import Base


class MembresiaClienteModel(Base):
    __tablename__ = "membresia_cliente"

    membresia_id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plan_suscripcion.plan_id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(String(20), nullable=False)

    cliente = relationship("ClienteModel", back_populates="membresias")
    plan = relationship("PlanSuscripcionModel", back_populates="membresias")
    pagos = relationship("PagoFacturaModel", back_populates="membresia")
