from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd.database import get_db
from app.schemas.response import StandardResponse
from app.schemas.reserva_inscripcion_schema import reservaInscripcionActualizar

from app.dependencies import requiere_rol
from app.routers.sesion_programada_router import get_reserva_service
from app.services.reserva_inscripcion_service import ReservaInscripcionService


router = APIRouter(prefix="/api/v1/reservas",
                    tags=["Gestión de Reservas de Inscripción"])
def get_reserva_service(db: AsyncSession = Depends(get_db)) -> ReservaInscripcionService:
    return ReservaInscripcionService(db)


@router.patch("/{id}",response_model=StandardResponse[reservaInscripcionActualizar], dependencies=[Depends(requiere_rol("Clientes"))])
async def cancelar_reserva_cliente(
    id: int, # Este 'id' mapea directamente al 'reserva_id'
    service: ReservaInscripcionService = Depends(get_reserva_service) # Tu service de reservas
):
    """
    Permite a los clientes cancelar una reserva existente cambiando su estado a 'cancelada'.
    """
    res = await service.cancelar_reserva(reserva_id=id)
    
    return {
        "status": "success",
        "message": "La reserva ha sido cancelada exitosamente",
        "data": res
    }