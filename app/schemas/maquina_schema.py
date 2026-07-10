from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
from typing import Optional
from datetime import date


#Hacemos la clase de una maquina inicial con todos los atributos necesarios
class maquinaInicial(BaseModel):
    categoria_id: int = Field(..., ge=1, description="ID de la categoría de la máquina")
    nombre: str = Field(..., max_length=100, description="Nombre de la máquina")
    descripcion_tecnica: Optional[str] = Field(None, description="Descripción técnica de la máquina")
    fecha_compra: Optional[date] = Field(None, description="Fecha de compra de la máquina")

#creamos una clase para la entrada de datos de la máquina, que hereda de la clase inicial y agrega el campo de fecha de instalaciónq
class maquinaCrear(maquinaInicial):
    pass

#Creamos una clase para los filtros de maquina, con un filtro por ID, nombre de su categoria y paginación
class MaquinaFiltros:
    def __init__(
        self,
        maquina_id: Optional[int] = Query(None, description="Filtrar por un ID específico"),
        nombre_categoria: Optional[str] = Query(None, description="Nombre de la categoría de la máquina"),
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Máquinas por página")
    ):
        self.maquina_id = maquina_id
        self.nombre_categoria = nombre_categoria
        self.page = page
        self.limit = limit

#Creamos una clase para la salida de datos de la máquina, que hereda de la clase inicial y agrega el campo de ID y estado operativo

class maquinaSalida(maquinaInicial):
    maquina_id: int = Field(..., description="ID de la máquina")
    estado_operativo: str = Field(..., description="Indica si la máquina está activa, fuera de servicio o en mantenimiento")
    model_config = ConfigDict(from_attributes=True)

#Creamos una clase para la actualización de datos de la máquina, que solo permite actualizar el estado de la maquina
class maquinaActualizar(BaseModel):
    estado_operativo: str = Field(..., description="Indica si la máquina está activa, fuera de servicio o en mantenimiento")