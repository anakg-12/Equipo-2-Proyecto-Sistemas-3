from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.schemas.venta_detalle_schema import VentaDetalleInicial, VentaDetalleSalida
from app.constants import SaleState

class VentaTiendaInicial(BaseModel):
    cliente_id: int = Field(..., ge=1, description="ID del cliente que realiza la compra")
    # fecha_venta se asigna automáticamente
    # total se calcula
    estado: SaleState = Field(SaleState.completada, description="Estado de la venta")

class VentaTiendaSalida(VentaTiendaInicial):
    venta_id: int = Field(..., description="ID de la venta")
    fecha_venta: datetime = Field(..., description="Fecha y hora de la venta")
    total: Decimal = Field(..., max_digits=10, decimal_places=2, description="Monto total de la venta", example=100.0)
    model_config = ConfigDict(from_attributes=True)

class VentaTiendaActualizar(BaseModel):
    estado: SaleState = Field(..., description="Nuevo estado de la venta")

class VentaTiendaFiltros:
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, ge=1, description="ID del cliente"),
        fecha_desde: Optional[datetime] = Query(None, description="Fecha inicial "), # formato ISO
        fecha_hasta: Optional[datetime] = Query(None, description="Fecha final "), # formato ISO
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Ventas por página")
    ):
        self.cliente_id = cliente_id
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.page = page
        self.limit = limit

class VentaCompletaEntrada(BaseModel):
    cliente_id: int
    monto_entregado: Decimal = Field(..., ge=0, description="Cantidad de dinero físico/dígital entregado por el cliente", example=100.0)
    items: list[VentaDetalleInicial]  # lista de productos con cantidad

class VentaCompletaSalida(VentaTiendaSalida):
    detalles: list[VentaDetalleSalida] = Field(..., description="Detalles de la venta")