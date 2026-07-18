from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.bd.database import Base
from enum import Enum

class RolesEnum(str, Enum):
    ADMINISTRACION = "Administracion"
    FINANZAS = "Finanzas"
    ENTRENADORES = "Entrenadores"
    CLIENTES = "Clientes"

class RolModel(Base):
    __tablename__ = "rol"

    rol_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)

    usuarios = relationship("UsuarioModel", back_populates="rol")