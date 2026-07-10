from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from fastapi import Query
from decimal import Decimal

#Hacemos la clase de un ticket de mantenimiento inicial con todos los atributos necesarios
class ticketMantenimiento(BaseModel):
    reportado_por: int = Field(..., ge=1, description="ID del administrador que reporta el problema")
    descripcion_falla: str = Field(..., description="Descripción de la falla")

#creamos una clase para la creacion de un ticket de mantenimiento
class ticketMantenimientoCrear(ticketMantenimiento):
    pass

#creamos una clase para la salida de un ticket de mantenimiento, que hereda de la clase inicial y agrega el campo de ID y estado del ticket
class ticketMantenimientoSalida(ticketMantenimiento):
    ticket_id: int
    maquina_id: int
    estado: str = Field(..., description="Indica si el ticket está abierto, en proceso o cerrado")
    fecha_resolucion: Optional[datetime] = Field(None, description="Fecha de resolución del ticket, si ya fue resuelto")
    costo_reparacion: Optional[Decimal] = Field(None, description="Costo de la reparación, si ya fue resuelto", example=200.0)
    model_config = ConfigDict(from_attributes=True)

#creamos una clase para cambiar el estado de un ticket de mantenimiento
class ticketMantenimientoActualizar(BaseModel):
    estado: str = Field(..., description="Indica si el ticket está abierto, en proceso o cerrado")

#creamos una clase para cambiar la fecha de resolución y el costo de reparación de un ticket de mantenimiento
class ticketMantenimientoResolver(BaseModel):
    fecha_resolucion: datetime = Field(..., description="Fecha de resolución del ticket")
    costo_reparacion: Decimal = Field(..., description="Costo de la reparación")

#creamos una clase para los filtros de ticket de mantenimiento
class ticketMantenimientoFiltros:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Tickets por página")
    ):
        self.page = page
        self.limit = limit