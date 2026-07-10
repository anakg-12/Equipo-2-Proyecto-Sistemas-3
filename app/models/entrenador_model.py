from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.bd.database import Base

class EntrenadorModel(Base):
    __tablename__ = "entrenador"

    entrenador_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.usuario_id", ondelete="CASCADE"), unique=True, nullable=False)
    especialidad = Column(String(100))
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)

    usuario = relationship("UsuarioModel", back_populates="entrenador")
    sesiones = relationship("SesionProgramadaModel", back_populates="entrenador")
    evaluaciones = relationship("EvaluacionBiometricaModel", foreign_keys="EvaluacionBiometricaModel.entrenador_id", back_populates="entrenador_asignado")