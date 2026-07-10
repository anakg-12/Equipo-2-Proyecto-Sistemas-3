from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import requiere_rol
from app.bd.database import get_db

from app.schemas.response import StandardResponse, PaginatedResponse

from app.schemas.producto_tienda_schema import (
    ProductoTiendaInicial,
    ProductoTiendaActualizar,
    ProductoTiendaFiltros,
    ProductoTiendaSalida
)

from app.services.producto_tienda_service import ProductoTiendaService

router = APIRouter(prefix="/api/v1/productos", tags=["Productos Tienda"])

def get_service(db: AsyncSession = Depends(get_db)) -> ProductoTiendaService:
    return ProductoTiendaService(db)

#hacemos el endpoint de crear
@router.post("/", response_model=StandardResponse[ProductoTiendaSalida], status_code=status.HTTP_201_CREATED, dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def crear_producto(schema: ProductoTiendaInicial, service: ProductoTiendaService = Depends(get_service)):
    """
    Crea un nuevo producto en la tienda. Requiere rol de Admin y Finanzas.
    """
    producto = await service.crear_producto(schema)
    return StandardResponse(status="success", message="Producto creado exitosamente", data=producto)

#hacemos el endpoint de actualizar
@router.patch("/{producto_id}", response_model=StandardResponse[ProductoTiendaSalida], dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def actualizar_producto(producto_id: int, schema: ProductoTiendaActualizar, service: ProductoTiendaService = Depends(get_service)):
    """
    Actualiza un producto existente. Requiere rol de Admin y Finanzas.
    Solo se pueden actualizar precio, stock.
    """
    producto = await service.actualizar_producto(producto_id, schema)
    return StandardResponse(status="success", message="Producto actualizado exitosamente", data=producto)

@router.get("/", response_model=PaginatedResponse[ProductoTiendaSalida])
async def listar_productos(
    filtros: ProductoTiendaFiltros = Depends(), 
    service: ProductoTiendaService = Depends(get_service)
):
    """Lista los productos de la tienda con filtros opcionales y paginación."""
    total, productos = await service.listar_productos(
        filtros.categoria, filtros.stock_min, filtros.page, filtros.limit
    )
    if total == 0:
        return {
            "total": total,
            "data": [],
            "page": filtros.page,
            "limit": filtros.limit,
            "message": "No se encontraron productos con los filtros proporcionados"
        }
    if total == 1:
        return {
            "total": total,
            "data": productos,
            "page": filtros.page,
            "limit": filtros.limit,
            "message": "1 producto encontrado con los filtros proporcionados"
        }
    return {
        "total": total,
        "data": productos,
        "page": filtros.page,
        "limit": filtros.limit,
        "message": "Productos obtenidos exitosamente" 
    }