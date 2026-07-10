from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

#hacemos la clase de un entrenador inicial con todos los atributos necesarios
class entrenadorInicial(BaseModel):
    usuario_id: int = Field(..., ge=1, description="ID del usuario del entrenador")
    especialidad: Optional[str] = Field(None, max_length=100, description="Especialidad del entrenador")
    telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono del entrenador")

#creamos una clase para la salida de datos del entrenador, que hereda de la clase inicial y agrega el campo de ID
class entrenadorSalida(entrenadorInicial):
    entrenador_id: int = Field(..., description="ID del entrenador")
    activo: bool = Field(..., description="Indica si el entrenador está activo")
    model_config = ConfigDict(from_attributes=True)

#creamos una clase para la actualización de datos del entrenador, que solo permite actualizar el campo de activo
class entrenadorActualizar(BaseModel):
    activo: bool = Field(..., description="Indica si el entrenador está activo")