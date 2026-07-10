from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


#Hacemos la clase de una plan de suscripcion inicial con todos los atributos necesarios
class planSuscripcionInicial(BaseModel):
    nombre: str = Field(..., max_length=50, description="Nombre del plan de suscripción")
    descripcion: Optional[str] = Field(None, description="Descripción del plan de suscripción")
    duracion_dias: int = Field(..., ge=1, description="Duración del plan de suscripción en días")
    costo: float = Field(..., ge=0, description="Costo del plan de suscripción")
    tipo: str = Field(..., max_length=20, description="Tipo de plan de suscripción (e.g., mensual, anual)")


#Creamos una clase para la entrada de datos del plan de suscripción, que hereda de la clase inicial
class planSuscripcionEntrada(planSuscripcionInicial):
    pass

#Creamos una clase para la salida de datos del plan de suscripción, que hereda de la clase inicial y agrega el campo de ID
class planSuscripcionSalida(planSuscripcionInicial):
    plan_id: int = Field(..., description="ID del plan de suscripción")
    activo: bool = Field(..., description="Indica si el plan de suscripción está activo")
    model_config = ConfigDict(from_attributes=True)

