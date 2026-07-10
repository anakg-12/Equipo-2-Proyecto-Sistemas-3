from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
from typing import Optional
from datetime import date

#Hacemos la clase de un cliente inicial con todos los atributos necesarios
class clienteInicial(BaseModel):
    usuario_id: int = Field(..., ge=1, description="ID del usuario asociado al cliente")
    telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono del cliente")
    direccion: Optional[str] = Field(None, description="Dirección del cliente")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento del cliente")

#Creamos una clase para los filtros de cliente, con un filtro por ID y paginación
class ClienteFiltros:
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="Filtrar por un ID específico"),
        activo: Optional[bool] = Query(None, description="Filtrar por estado de actividad del cliente"),
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Clientes por página")
    ):
        self.cliente_id = cliente_id
        self.page = page
        self.limit = limit
        self.activo = activo

#Creamos una clase para la salida de datos del cliente, que hereda de la clase inicial y agrega el campo de ID
class clienteSalida(clienteInicial):
    cliente_id: int = Field(..., description="ID del cliente")
    activo: bool = Field(..., description="Indica si el cliente está activo")
    model_config = ConfigDict(from_attributes=True)

#Creamos una clase para la actualización de datos del cliente, que solo permite actualizar el campo de activo
class clienteActualizar(BaseModel):
    activo: bool = Field(..., description="Indica si el cliente está activo")