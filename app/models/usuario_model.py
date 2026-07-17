from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.bd.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuario"

    usuario_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    rol_id = Column(
        Integer, ForeignKey("rol.rol_id", ondelete="RESTRICT"), nullable=False
    )
    activo = Column(Boolean, default=True)

    rol = relationship("RolModel", back_populates="usuarios")
    cliente = relationship("ClienteModel", back_populates="usuario", uselist=False)
    entrenador = relationship(
        "EntrenadorModel", back_populates="usuario", uselist=False
    )
