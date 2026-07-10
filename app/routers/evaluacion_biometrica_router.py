from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Infraestructura global del proyecto
from app.bd.database import get_db
from app.dependencies import requiere_rol
from app.schemas.response import StandardResponse, PaginatedResponse

# Importación de esquemas biométricos
from app.schemas.evaluacion_biometrica_schema import (
    EvaluacionBiometricaCrear,
    EvaluacionBiometricaSalida,
    EvaluacionBiometricaFiltros
)

# Importación del servicio encargado de la lógica de negocio
from app.services.evaluacion_biometrica_service import EvaluacionBiometricaService

# El prefijo se define como /api/v1/clientes para cumplir con el diseño de tus URLs
router = APIRouter(
    prefix="/api/v1/clientes",
    tags=["Módulo de Evaluación Biométrica"]
)

# Función inyectora para el servicio biométrico
def get_biometrico_service(db: AsyncSession = Depends(get_db)) -> EvaluacionBiometricaService:
    return EvaluacionBiometricaService(db)


@router.get("/{id}/evaluaciones", 
            response_model=PaginatedResponse[EvaluacionBiometricaSalida],
            dependencies=[Depends(requiere_rol(["Entrenadores"]))])
async def obtener_historial_evolucion(
    cliente_id: int,
    filtros: EvaluacionBiometricaFiltros = Depends(),
    service: EvaluacionBiometricaService = Depends(get_biometrico_service)
):
    """
    Retorna el historial métrico y biométrico de un cliente específico,
    ordenado cronológicamente.
    Accesible solo para Entrenadores.
    """
    skip = (filtros.page - 1) * filtros.limit
    
    total, res = await service.listar_evaluaciones(
        cliente_id=cliente_id, 
        skip=skip, 
        limit=filtros.limit
    )
    
    if total == 0:
        return {
            "status": "success",
            "message": "No se encontraron evaluaciones biométricas para este cliente",
            "data": [],
            "total": 0,
            "page": filtros.page,
            "limit": filtros.limit
        }
    
    return {
        "status": "success",
        "message": "Historial de evolución métrica obtenido exitosamente",
        "data": res,
        "total": total,
        "page": filtros.page,
        "limit": filtros.limit
    }


@router.post("/{id}/evaluaciones",
             status_code=status.HTTP_201_CREATED,
             response_model=StandardResponse[EvaluacionBiometricaSalida],
             dependencies=[Depends(requiere_rol("Entrenadores"))])
async def registrar_evaluacion_fisica(
    id: int,
    schema: EvaluacionBiometricaCrear,
    service: EvaluacionBiometricaService = Depends(get_biometrico_service)
):
    """
    Registra una nueva evaluación física periódica para un cliente específico
    (incluye peso, talla, estatura, porcentaje de grasa corporal y observaciones).
    Accesible únicamente para usuarios con el rol de Entrenadores.
    """
    res = await service.crear_evaluacion(cliente_id=id, schema=schema)
    
    return {
        "status": "success",
        "message": "Evaluación física registrada exitosamente",
        "data": res
    }