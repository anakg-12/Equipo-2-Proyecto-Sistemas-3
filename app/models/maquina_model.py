from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.bd.database import Base
from app.constants import MachineStatus

class MaquinaModel(Base):
    __tablename__ = "maquina"

    maquina_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion_tecnica = Column(Text)
    estado_operativo = Column(String(20), nullable=False, default=MachineStatus.activa.value)
    fecha_compra = Column(Date)
    categoria_id = Column(Integer, ForeignKey("categoria_maquina.categoria_id"), nullable=False)

    categoria = relationship("CategoriaMaquinaModel", back_populates="maquinas")
    tickets = relationship("TicketMantenimientoModel", back_populates="maquina")