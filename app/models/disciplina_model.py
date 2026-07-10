from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.bd.database import Base

class DisciplinaModel(Base):
    __tablename__ = "disciplina"

    disciplina_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text)

    sesiones = relationship("SesionProgramadaModel", back_populates="disciplina")