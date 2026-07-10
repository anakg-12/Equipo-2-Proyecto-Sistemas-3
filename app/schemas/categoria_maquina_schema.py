from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

#Hacemos la clase de una categoria de maquina inicial con todos los atributos necesarios
class categoriaMaquinaInicial(BaseModel):
    nombre: str = Field(..., max_length=50, description="Nombre de la categoría de la máquina")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría de la máquina")

#Creamos una clase para la salida de datos de la categoria de maquina, que hereda de la clase inicial y agrega el campo de ID
class categoriaMaquinaSalida(categoriaMaquinaInicial):
    categoria_id: int = Field(..., description="ID de la categoría de la máquina")
    model_config = ConfigDict(from_attributes=True)
