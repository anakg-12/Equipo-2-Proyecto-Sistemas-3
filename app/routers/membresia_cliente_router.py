from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import requiere_rol
from app.bd.database import get_db

from app.schemas.response import StandardResponse
from app.schemas.membresia_cliente_schema import (
    membresiaClienteCrear,
    membresiaClienteSalida,
)
from app.services.membresia_cliente_service import MembresiaClienteService

router = APIRouter(
    prefix="/api/v1/membresias",
    tags=["Módulo de Suscripción Activos"],
)

def get_service(db: AsyncSession = Depends(get_db)) -> MembresiaClienteService:
    return MembresiaClienteService(db)

@router.post("/", response_model=StandardResponse[membresiaClienteSalida], status_code=status.HTTP_201_CREATED, dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def crear_membresia_cliente(schema: membresiaClienteCrear, service: MembresiaClienteService = Depends(get_service)):
    """Crea una nueva membresia de cliente. Accesible para Administración y Finanzas."""
    result = await service.crear_membresia_cliente(schema)
    return {
        "status": "success",
        "message": "Membresía creada exitosamente",
        "data": result
    }

