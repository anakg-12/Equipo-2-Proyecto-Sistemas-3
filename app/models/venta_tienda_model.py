from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.bd.database import Base

class VentaTiendaModel(Base):
    __tablename__ = "venta_tienda"

    venta_id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)
    fecha_venta = Column(DateTime, server_default=func.now())
    total = Column(Numeric(10,2), nullable=False)
    estado = Column(String(20), nullable=False, default="completada")

    cliente = relationship("ClienteModel", back_populates="ventas")
    detalles = relationship("VentaDetalleModel", back_populates="venta", cascade="all, delete-orphan")