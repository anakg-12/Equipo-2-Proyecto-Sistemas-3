from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
from typing import Optional
from decimal import Decimal

class ProductoTiendaInicial(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    precio: Decimal = Field(..., max_digits=10, decimal_places=2, description="Precio unitario", example=100.0)
    stock: int = Field(..., description="Cantidad disponible en inventario")
    categoria: Optional[str] = Field(None, max_length=50, description="Categoría del producto (Accesorios, Suplementos)")

class ProductoTiendaSalida(ProductoTiendaInicial):
    producto_id: int = Field(..., description="ID del producto")
    model_config = ConfigDict(from_attributes=True)

class ProductoTiendaActualizar(BaseModel):
    precio: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2, description="Nuevo precio")
    stock: Optional[int] = Field(None, description="Nuevo stock")


class ProductoTiendaFiltros:
    def __init__(
        self,
        categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
        stock_min: Optional[int] = Query(None, gt=0, description="Stock mínimo"),
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Productos por página")
    ):
        self.categoria = categoria
        self.stock_min = stock_min
        self.page = page
        self.limit = limit