from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional

#Hacemos la clase de un cliente inicial con todos los atributos necesarios
class membresiaClienteInicial(BaseModel):
    cliente_id: int = Field(..., ge=1, description="ID del cliente asociado a la membresía")
    plan_id: Optional[int] = Field(None, ge=1, description="ID del plan de membresía")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio de la membresía")

class membresiaClienteCrear(membresiaClienteInicial):
    pass
#Creamos una clase que hereda de la clase inicial y agrega el campo de ID y estado activo
class membresiaClienteSalida(membresiaClienteInicial):
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin de la membresía")
    membresia_id: Optional[int] = Field(None, description="ID de la membresía del cliente")
    estado: str = Field(...,max_length=20, description="Indica el tipo de membresia que tiene el cliente")
    model_config = ConfigDict(from_attributes=True)



