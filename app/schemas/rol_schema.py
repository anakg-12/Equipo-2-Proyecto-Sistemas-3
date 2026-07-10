from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

#Hacemos la clase de un rol inicial con todos los atributos necesarios
class rolInicial(BaseModel):
    nombre: str = Field(..., max_length=50, description="Nombre del rol")
    descripcion: Optional[str] = Field(None, description="Descripción del rol")


#Creamos una clase para la salida de datos del rol, que hereda de la clase inicial y agrega el campo de ID
class rolSalida(rolInicial):
    rol_id: int = Field(..., description="ID del rol")
    model_config = ConfigDict(from_attributes=True)