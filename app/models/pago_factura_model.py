from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.bd.database import Base

class PagoFacturaModel(Base):
    __tablename__ = "pago_factura"

    pago_id = Column(Integer, primary_key=True)
    membresia_id = Column(Integer, ForeignKey("membresia_cliente.membresia_id"), nullable=False)
    monto = Column(Numeric(10,2), nullable=False)
    fecha_pago = Column(Date, server_default=func.current_date())
    metodo_pago = Column(String(30), nullable=False)
    referencia = Column(String(100))

    membresia = relationship("MembresiaClienteModel", back_populates="pagos")