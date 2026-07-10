from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

#Hacemos la clase de una categoria de maquina inicial con todos los atributos necesarios
class disciplinaInicial(BaseModel):
    nombre: str = Field(..., max_length=50, description="Nombre de la disciplina")
    descripcion: Optional[str] = Field(None, description="Descripción de la disciplina")

#Creamos una clase para la salida de datos de la categoria de maquina, que hereda de la clase inicial y agrega el campo de ID
class disciplinaSalida(disciplinaInicial):
    disciplina_id: int = Field(..., description="ID de la disciplina")
    model_config = ConfigDict(from_attributes=True)