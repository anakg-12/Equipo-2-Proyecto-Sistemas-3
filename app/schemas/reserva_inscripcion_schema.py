from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query
from datetime import datetime
from typing import Optional
from app.constants import ReservationState

#Hacemos la clase de una reserva de inscripcion inicial con todos los atributos necesarios
class reservaInscripcionInicial(BaseModel):
    sesion_id: int = Field(..., ge=1, description="ID de la sesión a la que se inscribe el cliente")
    fecha_reserva: Optional[datetime] = Field(None, description="Fecha de la reserva de inscripción")

#Creamos una clase para la entrada de datos de la reserva de inscripcion
class reservaInscripcionEntrada(reservaInscripcionInicial):
    pass
#Creamos una clase para la salida de datos de la reserva de inscripcion, que hereda de la clase inicial y agrega el campo de ID y estado de confirmación
class reservaInscripcionSalida(reservaInscripcionInicial):
    reserva_id: int = Field(..., description="ID de la reserva de inscripción")
    estado: ReservationState = Field(..., description="Indica el estado de la reserva de inscripcion")
    model_config = ConfigDict(from_attributes=True)

#Creamos una clase para actualizar el estado de la reserva de inscripción, con un campo para el nuevo estado
class reservaInscripcionActualizar(BaseModel):
    estado: ReservationState = Field(..., description="Nuevo estado de la reserva de inscripción")


#Creamos una clase para los filtros de reservas de clientes
class reservaInscripcionFiltros:
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="Filtrar por ID de cliente"),
        sesion_id: Optional[int] = Query(None, description="Filtrar por ID de sesión"),
        estado: Optional[ReservationState] = Query(None, description="Filtrar por estado de la reserva de inscripción"),
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Reservas de inscripción por página")
    ):
        self.cliente_id = cliente_id
        self.sesion_id = sesion_id
        self.estado = estado
        self.page = page
        self.limit = limit
#nuevo: 
class reservaInscripcionConSesionSalida(reservaInscripcionSalida):
    cliente_id: int = Field(..., ge=1, description="ID del cliente asociado a la reserva")
    nombre_sesion: str = Field(..., description="Nombre descriptivo de la sesión programada")