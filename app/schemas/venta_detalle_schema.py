from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class VentaDetalleInicial(BaseModel):
    producto_id: int = Field(..., ge=1, description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad vendida")
    precio_unitario: Decimal = Field(..., max_digits=10, decimal_places=2, description="Precio unitario en el momento de la venta", example=100.0)

class VentaDetalleSalida(VentaDetalleInicial):
    detalle_id: int = Field(..., description="ID del detalle")
    venta_id: int = Field(..., description="ID de la venta a la que pertenece")
    subtotal: Decimal = Field(..., max_digits=10, decimal_places=2, description="Subtotal (cantidad * precio_unitario)", example=100.0)
    model_config = ConfigDict(from_attributes=True)