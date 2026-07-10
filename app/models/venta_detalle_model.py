from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.bd.database import Base

class VentaDetalleModel(Base):
    __tablename__ = "venta_detalle"

    detalle_id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("venta_tienda.venta_id", ondelete="CASCADE"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto_tienda.producto_id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10,2), nullable=False)
    subtotal = Column(Numeric(10,2), nullable=False)  # aqui lo genera automaticamente la BD

    venta = relationship("VentaTiendaModel", back_populates="detalles")
    producto = relationship("ProductoTiendaModel", back_populates="detalles_ventas")