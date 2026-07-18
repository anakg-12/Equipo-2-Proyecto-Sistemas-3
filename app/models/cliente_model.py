from sqlalchemy import Column, Integer, String, Boolean, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.bd.database import Base


class ClienteModel(Base):
    __tablename__ = "cliente"

    cliente_id = Column(Integer, primary_key=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuario.usuario_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    direccion = Column(Text)
    fecha_nacimiento = Column(Date)
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)

    usuario = relationship("UsuarioModel", back_populates="cliente")
    reservas = relationship("ReservaInscripcionModel", back_populates="cliente")
    accesos = relationship("ControlAccesoModel", back_populates="cliente")
    membresias = relationship("MembresiaClienteModel", back_populates="cliente")
    ventas = relationship("VentaTiendaModel", back_populates="cliente")
    evaluaciones = relationship(
        "EvaluacionBiometricaModel", back_populates="cliente_evaluado"
    )
