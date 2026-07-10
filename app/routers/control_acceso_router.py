from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import requiere_rol
from app.bd.database import get_db


from app.schemas.control_acceso_schema import (
controlAccesoEntrada, 
controlAccesoSalida
)

from app.services.control_acceso_service import ControlAccesoService
from app.schemas.response import StandardResponse

router = APIRouter(
    prefix="/api/v1/control_acceso", tags=["Control de Acceso"])

def get_service(db: AsyncSession = Depends(get_db)) -> ControlAccesoService:
    return ControlAccesoService(db) 

@router.post("/entrada", 
             status_code=status.HTTP_200_OK,
             response_model=StandardResponse[controlAccesoSalida],
             # Aquí asumo que tu función de seguridad puede recibir una lista de roles.
             # Si solo recibe uno, te dejo una nota abajo de cómo manejarlo.
             dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def procesar_entrada_gimnasio(
    schema: controlAccesoEntrada, 
    service: ControlAccesoService = Depends(get_service)
):
    """
    Recibe cédula y valida membresía 'Activa' o 'Por vencer' para permitir ingreso.
    Este endpoint representa la recepción del gimnasio.
    Accesible por Administración y Finanzas.
    """
    
    # IMPORTANTE: La validación de si la membresía está "Activa" o "Por vencer" 
    # NO se hace aquí en el router. Se hace dentro del servicio.
    res = await service.registrar_y_validar_entrada(schema)
    
    return {
        "status": "success",
        "message": "Proceso de acceso evaluado con éxito",
        "data": res
    }