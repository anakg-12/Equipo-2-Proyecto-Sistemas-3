from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import requiere_rol
from app.bd.database import get_db

from app.schemas.response import StandardResponse
from app.schemas.pago_factura_schema import (
    pagoFacturaSalida,
    pagoFacturaEntrada
    )
from app.services.pago_factura_services import PagoFacturaService
router = APIRouter(prefix="/api/v1/pagos",
                    tags=["Módulo de Suscripción Activos"])

def get_service(db: AsyncSession = Depends(get_db)) -> PagoFacturaService:
    return PagoFacturaService(db)

@router.post("/", status_code=status.HTTP_201_CREATED,
              response_model=StandardResponse[pagoFacturaSalida],
              dependencies=[Depends(requiere_rol("Finanzas"))])
async def crear_pago_factura(schema: pagoFacturaEntrada, service: PagoFacturaService = Depends(get_service)):
    "Registra un nuevo pago de factura. Solo accesible para usuarios con rol de Finanzas."
    res, vuelto = await service.create_pago_factura(schema)
    return {
        "status": "success",
        "message": f"Pago de factura registrado exitosamente. Vuelto a entregar: ${vuelto}",
        "data": res
    }
    