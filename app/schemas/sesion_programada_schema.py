from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi import Query
from datetime import datetime, date
from enum import Enum

class estadosSesion(str, Enum):
    programada = "programada"
    completada = "completada"
    cancelada = "cancelada"

#Hacemos la clase de una sesión programada inicial con todos los atributos necesarios
class sesionProgramadaInicial(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre de la clase")
    disciplina_id: int = Field(..., ge=1, description="ID de la disciplina asociada a la sesión programada")
    entrenador_id: int = Field(..., ge=1, description="ID del entrenador asociado a la sesión programada")
    fecha_hora_inicio: datetime = Field(..., description="Fecha y hora de inicio de la sesión programada")
    fecha_hora_fin: datetime = Field(..., description="Fecha y hora de fin de la sesión programada")
    cupo_maximo: int = Field(..., ge=1, description="Cupo máximo de participantes en la sesión programada") 
    ubicacion: Optional[str] = Field(None, max_length=100, description="Ubicación de la sesión programada")

#Creamos una clase para los filtros de sesión programada, con un filtro de su estado, por su fecha, por su disciplina y que el entrenador vea las sesiones asociadas a el
class SesionProgramadaFiltros:
    def __init__(
        self,
        estado: Optional[str] = Query(None, description="Filtrar por estado de la sesión programada (programada, completada, cancelada)"),
        fecha: Optional[date] = Query(None, description="Filtrar por fecha de la sesión programada"),
        disciplina_id: Optional[int] = Query(None, description="Filtrar por ID de la disciplina asociada a la sesión programada"),
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Sesiones programadas por página")
    ):
        self.estado = estado
        self.fecha = fecha
        self.disciplina_id = disciplina_id
        self.page = page
        self.limit = limit

#Creamos una clase para la entrada de datos de la sesión programada, que hereda de la clase inicial
class sesionProgramadaEntrada(sesionProgramadaInicial):
    pass

#Creamos una clase para la salida de datos de la sesión programada, que hereda de la clase inicial y agrega el campo de ID y estado
class sesionProgramadaSalida(sesionProgramadaInicial):
    sesion_id: int = Field(..., description="ID de la sesión programada")
    estado: estadosSesion = Field(..., description="Indica si la sesion esta programada, completada o cancelada")
    model_config = ConfigDict(from_attributes=True)

#Creamos una clase para la actualización de datos de la sesión programada, que solo permite actualizar el campo de estado
class sesionProgramadaActualizar(BaseModel):
    estado: estadosSesion = Field(..., description="Indica si la sesion esta programada, completada o cancelada")