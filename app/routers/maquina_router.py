from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

#from sqlalchemy.orm import Session  ## este debe ser como el traducctor de la db


from app.dependencies import requiere_rol
from app.bd.database import get_db
from app.schemas.response import StandardResponse, PaginatedResponse


from app.schemas.maquina_schema import ( 
    maquinaCrear, 
    maquinaSalida, 
    maquinaActualizar, 
    MaquinaFiltros,
    )  

from app.schemas.ticket_mantenimiento_schema import (
    ticketMantenimientoCrear,
    ticketMantenimientoSalida,
    ticketMantenimientoFiltros
    )

from app.services.maquina_service import maquinaService #esto es para que
# que traer info sobre si la maquina está en servivicio/funcional o no
from app.services.ticket_mantenimiento_service import TicketMantenimientoService

router = APIRouter(prefix="/api/v1/maquinas",
                    tags=["Módulo de Inventario de Máquinas"])

def get_service(db: AsyncSession = Depends(get_db)) -> maquinaService: 
    return maquinaService(db)

def get_ticket_service(db: AsyncSession = Depends(get_db)) -> TicketMantenimientoService:
    return TicketMantenimientoService(db)

@router.get("/", response_model=PaginatedResponse[maquinaSalida])
async def listar_maquinas(
    filtros: MaquinaFiltros = Depends(), 
    service: maquinaService = Depends(get_service)
):
    """
    Lista las maquinas, soporta filtrado por ID y categoría. 
    Accesible para cualquier Usuario.
    """

    skip = (filtros.page - 1) * filtros.limit
    total, res = await service.list_maquinas(
        id=filtros.maquina_id,
        categoria_nombre=filtros.nombre_categoria, 
        skip=skip, 
        limit=filtros.limit
    )
    if total == 0:
        return {
            "status": "success",
            "message": "No se encontraron máquinas con los filtros proporcionados",
            "data": [],
            "total": 0,
            "page": filtros.page,
            "limit": filtros.limit
        }
    if total == 1:
        return {
            "status": "success",
            "message": "Máquina obtenida exitosamente",
            "data": res,
            "total": total,
            "page": filtros.page,
            "limit": filtros.limit
        }
    return {
        "status": "success",
        "message": "Lista de máquinas obtenida exitosamente",
        "data": res,
        "total": total,
        "page": filtros.page,
        "limit": filtros.limit
    }

@router.get("/{id}", response_model=StandardResponse[maquinaSalida])
async def obtener_maquina(id: int, service: maquinaService = Depends(get_service)):

    """
    Lista maquinas por su ID.
    Accesible para todos los usuarios.
    """

    res= await service.get_maquina(id)

    return {
        "status": "success",
        "message": "Máquina encontrada",
        "data": res
    }

@router.post("/", status_code=status.HTTP_201_CREATED,
              response_model=StandardResponse[maquinaSalida],
                dependencies=[Depends(requiere_rol("Administracion"))])
async def registrar_maquina(schema: maquinaCrear, service: maquinaService = Depends(get_service)):
    "Registra una nueva máquina. Solo accesible para usuarios con rol de Administracion."
    res = await service.create_maquina(schema)
    return {
        "status": "success",
        "message": "Máquina registrada exitosamente",
        "data": res
    }

@router.patch("/{id}/estado", response_model=StandardResponse[maquinaSalida],
              dependencies=[Depends(requiere_rol("Administracion"))])
async def actualizar_estado_maquina(
    id: int, 
    schema: maquinaActualizar, 
    service: maquinaService = Depends(get_service)):

    """
    Actualiza el estado de una máquina (activa, mantenimiento, fuera de servicio).
    Solo accesible para usuarios con rol de Administración.
    """

    res = await service.update_maquina_estado(id, schema)
    return {
        "status": "success",
        "message": "Estado de la máquina actualizado exitosamente",
        "data": res
    }

@router.post("/{id}/tickets",status_code=status.HTTP_201_CREATED,
              response_model=StandardResponse[ticketMantenimientoSalida],
                dependencies=[Depends(requiere_rol("Administracion"))])
async def abrir_ticket_reparacion(
    id: int,
    schema: ticketMantenimientoCrear,
    service: TicketMantenimientoService = Depends(get_ticket_service)
): 
    """
    Abre un ticket de reparación de una máquina específica y cambia el estado 
    operativo de la máquina a 'en mantenimiento' o 'fuera de servicio'.
    Solo accesible para usuarios con rol de Administración.
    """
    # Llamamos a una función en el servicio que se encargue de ambas cosas a la vez
    res = await service.crear_ticket_y_actualizar_maquina(id, schema)
    return {
        "status": "success",
        "message": "Ticket de reparación abierto y estado de la máquina actualizado exitosamente",
        "data": res
    }

@router.get("/{id}/tickets", response_model=PaginatedResponse[ticketMantenimientoSalida],
            dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def consultar_tickets_maquina(
    id: int,
    filtros: ticketMantenimientoFiltros = Depends(),
    service: TicketMantenimientoService = Depends(get_ticket_service),
   

):
    """
    Consulta la bitácora de reparaciones y costos de una máquina específica.
    Accesible solo para usuarios con rol de Administración o Finanzas.
    """
    skip = (filtros.page - 1) * filtros.limit

    # Llamamos a la función del servicio que buscará el historial en la base de datos
    total, res = await service.list_tickets_maquina(maquina_id=id, skip=skip, limit=filtros.limit)

    if total == 0:
        return {
            "status": "success",
            "message": "No se encontraron tickets de reparación para esta máquina",
            "data": [],
            "total": 0,
            "page": filtros.page,
            "limit": filtros.limit
        }

    return {
        "status": "success",
        "message": "Bitácora de reparaciones obtenida exitosamente",
        "data": res,
        "total": total,
        "page": filtros.page,
        "limit": filtros.limit
    }