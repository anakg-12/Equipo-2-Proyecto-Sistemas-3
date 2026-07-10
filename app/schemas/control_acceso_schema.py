from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

#Hacemos la clase de un control de acceso inicial con todos los atributos necesarios
class controlAccesoInicial(BaseModel):
    cliente_id: int = Field(..., ge=1, description="ID del cliente que accede al gimnasio")
    fecha_hora_entrada: Optional[datetime] = Field(None, description="Fecha y hora de entrada al gimnasio")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales sobre el acceso del cliente")

#Creamos una clase para la entrada de datos del control de acceso, que hereda de la clase inicial y agrega el campo de fecha y hora de salida
class controlAccesoEntrada(BaseModel):
    cedula: str = Field(..., max_length=12, description="Cédula del cliente que accede al gimnasio")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales sobre el acceso del cliente")

#Creamos una clase para la salida de datos del control de acceso, que hereda de la clase inicial y agrega el campo de ID y fecha de salida
class controlAccesoSalida(controlAccesoInicial):
    acceso_id: int = Field(..., description="ID del control de acceso")
    validado: Optional[bool] = Field(None, description="Indica si el acceso fue validado correctamente")
    model_config = ConfigDict(from_attributes=True)