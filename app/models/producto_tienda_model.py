from sqlalchemy import Column, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from app.bd.database import Base

class ProductoTiendaModel(Base):
    __tablename__ = "producto_tienda"

    producto_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10,2), nullable=False)
    stock = Column(Integer, nullable=False)
    categoria = Column(String(50))

    detalles_ventas = relationship("VentaDetalleModel", back_populates="producto")