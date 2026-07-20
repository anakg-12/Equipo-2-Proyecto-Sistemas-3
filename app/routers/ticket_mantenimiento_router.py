from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Dependencias e infraestructura global del proyecto
from app.bd.database import get_db
from app.dependencies import requiere_rol
from app.schemas.response import StandardResponse

# Importación de esquemas (Ajusta los nombres si en tu archivo se llaman diferente)
from app.schemas.ticket_mantenimiento_schema import (
    ticketMantenimientoSalida,
    ticketMantenimientoActualizar,
    ticketMantenimientoResolver
    
)

# Importación del servicio correspondiente
from app.services.ticket_mantenimiento_service import TicketMantenimientoService

# Inicializamos el enrutador con su prefijo y etiquetas para Swagger
router = APIRouter(
    prefix="/api/v1/tickets",
    tags=["Gestión de Tickets de Mantenimiento"])

# Función inyectora para obtener el servicio de tickets
def get_ticket_service(db: AsyncSession = Depends(get_db)) -> TicketMantenimientoService:
    return TicketMantenimientoService(db)


@router.patch("/{id}/estado", 
              response_model=StandardResponse[ticketMantenimientoSalida],
              dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def actualizar_estado_ticket(
    id: int,
    schema: ticketMantenimientoActualizar,
    service: TicketMantenimientoService = Depends(get_ticket_service)
):
    """
    Permite actualizar el estado del ticket de mantenimiento.
    Estados permitidos: "abierto", "en_proceso", "cerrado".
    Accesible solo para usuarios con rol de Administración y Finanzas.
    """
    from app.constants import TICKET_STATES as estados_permitidos
    # estados_permitidos = ["abierto", "en_proceso", "cerrado"]
    
    if schema.estado.value not in estados_permitidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado '{schema.estado}' no es válido. Opciones permitidas: {', '.join(estados_permitidos)}"
        )
        
    res = await service.actualizar_ticket(id, schema)
    
    return {
        "status": "success",
        "message": "Estado del ticket actualizado exitosamente",
        "data": res
    }


@router.patch("/{id}/resolucion", 
              response_model=StandardResponse[ticketMantenimientoSalida],
              dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def registrar_resolucion_ticket(
    id: int,
    schema: ticketMantenimientoResolver,
    service: TicketMantenimientoService = Depends(get_ticket_service)
):
    """
    Permite registrar el costo de reparación y la fecha de resolución 
    al momento de finalizar el mantenimiento del equipo.
    Accesible solo para usuarios con rol de Administración y Finanzas.
    """
    res = await service.resolver_ticket(id, schema)
    res = await service.resolver_ticket(id, schema)
    
    return {
        "status": "success",
        "message": "Resolución y costos del ticket registrados exitosamente",
        "data": res
    }