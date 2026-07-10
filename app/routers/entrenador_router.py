from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, requiere_rol
from app.bd.database import get_db
from app.schemas.response import PaginatedResponse, StandardResponse

from app.schemas.entrenador_schema import entrenadorActualizar, entrenadorInicial, entrenadorSalida
from app.schemas.sesion_programada_schema import sesionProgramadaSalida

from app.services.entrenador_service import entrenadorService
from app.services.sesion_programada_service import SesionProgramadaService

router = APIRouter(prefix="/api/v1/entrenadores", 
                   tags=["Entrenadores"])

def get_service(db: AsyncSession = Depends(get_db)) -> entrenadorService:
    return entrenadorService(db)

def get_sesion_service(db: AsyncSession = Depends(get_db)) -> SesionProgramadaService:
    return SesionProgramadaService(db)

@router.post("/",
            response_model=StandardResponse[entrenadorSalida],
            dependencies=[Depends(requiere_rol("Administracion"))])
async def crear_entrenador(
    schema: entrenadorInicial,
    service: entrenadorService = Depends(get_service)
):
    """
    Crea un nuevo entrenador. 
    Solo accesible para Administración.
    """
    res = await service.create_entrenador(schema)
    
    return {
        "status": "success",
        "message": "Entrenador creado exitosamente",
        "data": res
    }
@router.patch("/{id}/estado", 
              response_model=StandardResponse[entrenadorSalida],
              dependencies=[Depends(requiere_rol("Administracion"))])
async def actualizar_estado_entrenadores(
    id: int,
    schema: entrenadorActualizar,
    service: entrenadorService = Depends(get_service)
):
    """
    Permite actualizar el estado como entrenador, para gestionar 
    su disponibilidad de forma independiente a su usuario.
    Solo accesible para Administración.
    """
    # Pasamos el ID y el esquema validado directamente a la capa de servicios
    res = await service.update_estado_entrenador(id, schema) # Aquí asumimos que el cambio es para activar, pero podrías ajustar según tus necesidades
    
    return {
        "status": "success",
        "message": "Disponibilidad del entrenador actualizada exitosamente",
        "data": res
    }    
@router.get("/me/sesiones", 
            response_model=PaginatedResponse[sesionProgramadaSalida])
async def listar_sesiones_entrenador(
    page: int = 1,
    limit: int = 20,
    usuario_actual: entrenadorSalida = Depends(get_current_user),
    service: SesionProgramadaService = Depends(get_sesion_service)
):
    """
    Permite a los entrenadores listar las sesiones programadas donde ellos se encuentren.
    Solo accesible para Entrenadores.
    """
    total, res = await service.listar_sesiones_usuario(usuario_id=usuario_actual.usuario_id, page=page, limit=limit)
    
    if total == 0:
        return {
            "status": "success",
            "message": "No se encontraron sesiones programadas para este entrenador",
            "data": res,
            "total": total,
            "page": page,
            "limit": limit
        }
    if total == 1:
        return {
            "status": "success",
            "message": "Sesión programada obtenida exitosamente",
            "data": res,
            "total": total,
            "page": page,
            "limit": limit
        }
    return {
        "status": "success",
        "message": "Sesiones obtenidas exitosamente",
        "data": res,
        "total": total,
        "page": page,
        "limit": limit
    }