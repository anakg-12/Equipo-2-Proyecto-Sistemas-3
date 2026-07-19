from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

#from sqlalchemy.orm import Session  ## este debe ser como el traducctor de la db

from app.dependencies import requiere_rol
from app.bd.database import get_db
from app.schemas.reserva_inscripcion_schema import reservaInscripcionActualizar
from app.schemas.response import StandardResponse, PaginatedResponse

from app.schemas.sesion_programada_schema import (
    sesionProgramadaEntrada,
    sesionProgramadaSalida,
    sesionProgramadaActualizar,
    SesionProgramadaFiltros
    )


from app.services.sesion_programada_service import SesionProgramadaService 
from app.services.reserva_inscripcion_service import ReservaInscripcionService

router = APIRouter(prefix="/api/v1/sesiones",
                    tags=["Gestión de Sesiones Programadas"])

def get_service(db: AsyncSession = Depends(get_db)) -> SesionProgramadaService:
    return SesionProgramadaService(db)

def get_reserva_service(db: AsyncSession = Depends(get_db)) -> ReservaInscripcionService:
    return ReservaInscripcionService(db)

@router.get("/", response_model=PaginatedResponse[sesionProgramadaSalida] )
async def listar_sesiones(
    filtros: SesionProgramadaFiltros = Depends(),
    service: SesionProgramadaService = Depends(get_service)
):
   """
   Lista clases disponibles con filtros de fecha, disciplina y estado.
   Soporta diferentes filtrados- Accesible para usuarios.
   """
   skip = (filtros.page - 1) * filtros.limit
    
   total, res = await service.list_sesiones(
        estado=filtros.estado,
        fecha=filtros.fecha,
        disciplina_id=filtros.disciplina_id,
        skip=skip,
        limit=filtros.limit
    )
   
   mensaje_respuesta  = "Sesiones obtenidas con éxito"
   
   if total == 0:
       mensaje_respuesta = "No se encontraron sesiones que coincidan con las características solicitadas"
   
   if total == 1:
       mensaje_respuesta = "Sesión obtenida con éxito"
   return {
        "status": "success",
        "message": mensaje_respuesta,
        "data": res,
        "total": total,
        "page": filtros.page,
        "limit": filtros.limit
    }

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=StandardResponse[sesionProgramadaSalida],
             dependencies=[Depends(requiere_rol("Administracion"))])
async def programar_sesion(
    schema: sesionProgramadaEntrada,
    service: SesionProgramadaService = Depends(get_service)
):
    """Programa una nueva sesión de clase. Accesible para Administración.
    """
    res = await service.create_sesion(schema)
    return {
        "status": "success",
        "message": "Sesión programada con éxito",
        "data": res
    }

@router.patch("/{id}/estado",
              response_model=StandardResponse[sesionProgramadaSalida],
              dependencies=[Depends(requiere_rol("Administracion"))])
async def actualizar_estado_sesion(
    id: int,
    schema: sesionProgramadaActualizar,
    service: SesionProgramadaService = Depends(get_service)
):
    """Actualiza el estado de una sesión (programada, cancelada o completada), 
    Incluye validación manual de estados permitidos.
    Accesible para Administración.
    """
    from app.constants import SESSION_STATES as estados_permitidos
    # estados_permitidos = ["programada", "completada", "cancelada"]

    if schema.estado.value not in estados_permitidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado '{schema.estado}' no es válido. Opciones: {', '.join(estados_permitidos)}"
        )
    
    res = await service.update_sesion_estado(id, schema)
    return {
        "status": "success",
        "message": "Estado de sesión actualizado exitosamente",
        "data": res
    }

@router.get("/{id}/reservas",
            dependencies=[Depends(requiere_rol("Entrenadores"))])
async def consultar_reservas_sesion(
    id: int,
    reserva_service: ReservaInscripcionService = Depends(get_reserva_service)
):
    """Permite al entrenador consultar los inscritos en su clase.
    Accesible para Entrenador"""
    res = await reserva_service.obtener_inscritos_por_sesion(id)

    if len(res) == 0:
       mensaje = "No hay reservas activas en esta sesión todavía"
    else: 
       mensaje = "Lista de inscritos obtenida con éxito"

       mensaje_respuesta = "Sesión obtenida con éxito"

    return {
        "status": "success",
        "message": mensaje,
        "data": res
    }
@router.patch("/{id}/reservas/{cliente_id}", dependencies=[Depends(requiere_rol("Entrenadores"))])
async def marcar_asistencia_clase(
    id: int,
    cliente_id: int,
    schema: reservaInscripcionActualizar,
    reserva_service: ReservaInscripcionService = Depends(get_reserva_service)
):
    """Permite al entrenador marcar la asistencia de un cliente a su clase (activa, cancelada o asistio),
    ingresando el ID de la sesión y el cliente_id. 
    Accesible solo para Entrenador
    
    """
    res = await reserva_service.actualizar_estado_reserva(sesion_id=id, cliente_id=cliente_id, schema=schema)
    return {
        "status": "success",
        "message": "Asistencia actualizada exitosamente",
        "data": res
    }