from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from decimal import Decimal
from app.constants import PayMethod

#Hacemos la clase de una pago de factura inicial con todos los atributos necesarios
class pagoFacturaInicial(BaseModel):
    membresia_id: int = Field(..., ge=0, description="ID de la membresía")
    monto: Decimal = Field(...,  max_digits=10, decimal_places=2, gt=0, description="Monto del pago", example=200.0)
    metodo_pago: PayMethod = Field(..., min_length=1, description="Método de pago")
    fecha_pago: Optional[date] = Field(..., description="Fecha del pago")
    referencia: Optional[str] = Field(None, description="Referencia del pago, si es que se requiere")

#Creamos una clase para la entrada de datos del pago de factura, que hereda de la clase inicial
class pagoFacturaEntrada(pagoFacturaInicial):
    pass
#Creamos una clase para la salida de datos del pago de factura, que hereda de la clase inicial y agrega el campo de ID
class pagoFacturaSalida(pagoFacturaInicial):
    pago_id: int = Field(..., description="ID del pago de factura")
    model_config = ConfigDict(from_attributes=True)