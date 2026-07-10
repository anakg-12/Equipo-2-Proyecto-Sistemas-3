from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import requiere_rol
from app.bd.database import get_db

#from sqlalchemy.orm import Session  ## este debe ser como el traducctor de la db
from app.schemas.response import PaginatedResponse, StandardResponse

from app.schemas.plan_suscripcion_schema import (
    planSuscripcionSalida
    ) 

from app.services.plan_suscripcion_service import PlanService

router = APIRouter(prefix="/api/v1/planes",
                    tags=["Módulo de Suscripción Activos"])

def get_service(db: AsyncSession = Depends(get_db)) -> PlanService: 
    return PlanService(db)

@router.get("/", response_model=PaginatedResponse[planSuscripcionSalida])
async def listar_planes(page: int = Query(1, ge=1), 
                        limit: int = Query(10, ge=1, le=100), 
                        service: PlanService = Depends(get_service)):
    
    """
    Listado de planes de suscripción con costo y duración, para oferta comercial.
    Accesible para todos. 
    """
    skip = (page - 1) * limit
    total, res = await service.list_planes(skip, limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "page": page,
        "limit": limit
    }