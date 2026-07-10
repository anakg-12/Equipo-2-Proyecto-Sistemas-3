from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.bd.database import Base

class CategoriaMaquinaModel(Base):
    __tablename__ = "categoria_maquina"

    categoria_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)

    maquinas = relationship("MaquinaModel", back_populates="categoria")