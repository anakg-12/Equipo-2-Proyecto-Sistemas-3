from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List 

T = TypeVar('T') 

class StandardResponse(BaseModel, Generic[T]):
    #estructura para respuestas cortas/simples (un solo objeto)
    status: str
    message: str
    data: Optional[T] = None

class PaginatedResponse(BaseModel, Generic[T]):
    #estructura para respuestas con multiples elemetos y paginación.
    status: str = "success"
    message: str
    data: List[T]
    total: int
    page: int 
    limit: int


    #return {
    #    "status": "success",
    #    "message": "Sesiones obtenidas con éxito",
     #   "data": res,
    #    "total": total,
    #    "page": filtros.page, # <-- CAMBIO AQUÍ: de 'skip' a 'page'
    #    "limit": filtros.limit
   # }"""

   #nueva clase para cumplir reglas estrictas de error....
class ErrorResponse(BaseModel):
    """
    Estructura estricta para los errores HTTP 400, 404, 409, etc.
    """
    error: str
    codigoInterno: str
    mensaje: str
    timestamp: str
