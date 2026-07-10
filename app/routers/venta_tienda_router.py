from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Infraestructura global del proyecto
from app.bd.database import get_db
from app.dependencies import requiere_rol
from app.schemas.response import StandardResponse, PaginatedResponse

# Importación de esquemas de ventas
from app.schemas.venta_tienda_schema import (
    VentaCompletaEntrada,
    VentaTiendaSalida,
    VentaTiendaFiltros
)

# Importación del servicio de ventas
from app.services.venta_tienda_service import VentaTiendaService

# Definimos el prefijo /api/v1/ventas
router = APIRouter(
    prefix="/api/v1/ventas",
    tags=["Módulo de Ventas y Tienda"]
)

# Función inyectora para el servicio
def get_ventas_service(db: AsyncSession = Depends(get_db)) -> VentaTiendaService:
    return VentaTiendaService(db)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=StandardResponse[VentaTiendaSalida],
             dependencies=[Depends(requiere_rol("Finanzas"))])
async def registrar_venta(
    schema: VentaCompletaEntrada,
    service: VentaTiendaService = Depends(get_ventas_service)
):
    """
    Registra una nueva venta, descuenta automáticamente el stock de los productos
    y genera el ingreso en el sistema financiero. Calcula e informa el vuelto correspondiente.
    Accesible únicamente para usuarios con el rol de Finanzas.
    """
    venta, vuelto = await service.registrar_venta(schema)

    return {
        "status": "success",
        "message": f"Venta registrada exitosamente. Vuelto a entregar: ${vuelto}",
        "data": venta
    }

@router.get("/",
            response_model=PaginatedResponse[VentaTiendaSalida],
            dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def listar_historial_ventas(
    filtros: VentaTiendaFiltros = Depends(),
    service: VentaTiendaService = Depends(get_ventas_service)
):
    """
    Lista el historial de ventas del gimnasio. 
    Soporta filtrado por cliente y rangos de fecha (fecha_desde, fecha_hasta).
    Accesible solo para Administración y Finanzas.
    """
    skip = (filtros.page - 1) * filtros.limit

    # Asumimos que tu repositorio retorna (total, registros) como en los otros módulos
    total, res = await service.listar_ventas(
        cliente_id=filtros.cliente_id,
        fecha_desde=filtros.fecha_desde,
        fecha_hasta=filtros.fecha_hasta,
        skip=skip,
        limit=filtros.limit
    )

    # Manejo de la respuesta cuando no hay ventas que coincidan con el filtro
    if total == 0:
        return {
            "status": "success",
            "message": "No se encontraron ventas en este rango de fechas o con este cliente",
            "data": [],
            "total": 0,
            "page": filtros.page,
            "limit": filtros.limit
        }

    return {
        "status": "success",
        "message": "Historial de ventas obtenido exitosamente",
        "data": res,
        "total": total,
        "page": filtros.page,
        "limit": filtros.limit
    }