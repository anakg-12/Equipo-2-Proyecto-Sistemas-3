from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.bd.database import Base
from app.constants import SessionState

class  SesionProgramadaModel(Base):
    __tablename__ = "sesion_programada"

    sesion_id = Column(Integer, primary_key=True)
    disciplina_id = Column(Integer, ForeignKey("disciplina.disciplina_id"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("entrenador.entrenador_id"), nullable=False)
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=False)
    cupo_maximo = Column(Integer, nullable=False)
    ubicacion = Column(String(100))
    nombre = Column(String(100), nullable=True)
    estado = Column(String(20), nullable=False, default=SessionState.programada.value)

    disciplina = relationship("DisciplinaModel", back_populates="sesiones")
    entrenador = relationship("EntrenadorModel", back_populates="sesiones")
    reservas = relationship("ReservaInscripcionModel", back_populates="sesion")