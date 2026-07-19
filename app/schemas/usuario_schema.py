from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator # Field_validator para validar la contraseña :)
from fastapi import Query
from typing import Optional


#Hacemos la clase de un usuario inicial con todos los atributos necesarios
class usuarioInicial(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nickname de usuario")
    email: EmailStr = Field(..., min_length=3, max_length=100, description="Correo electronico del usuario")
    cedula: str = Field(..., min_length=3, max_length=20, description="Cédula del usuario")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    apellido: str = Field(..., min_length=3, max_length=50, description="Apellido del usuario")
    rol_id: int = Field(..., ge=1, description="ID del rol del usuario")

#Creamos una clase para los filtros de usuario, con un filtro por ID y paginación
class UsuarioFiltros:
    def __init__(
        self,
        usuario_id: Optional[int] = Query(None, description="Filtrar por un ID específico"),
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Usuarios por página")
    ):
        self.usuario_id = usuario_id
        self.page = page
        self.limit = limit

#Creamos una clase para la entrada de datos del usuario, que hereda de la clase inicial y agrega el campo de contraseña
class usuarioEntrada(usuarioInicial):
    password_recibida: str = Field(..., min_length=3, max_length=255, description="Contraseña del usuario")

    # Validador para la contraseña, que verifica que tenga al menos 8 caracteres y que incluya números y letras :)
    @field_validator('password_recibida')
    @classmethod
    def validar_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("La contraseña es muy débil. Debe tener al menos 8 caracteres e incluir números y letras")
        if not any(char.isalpha() for char in value) or not any(char.isdigit() for char in value):
            raise ValueError("La contraseña es muy débil. Debe tener al menos 8 caracteres e incluir números y letras")
        return value

#Creamos una clase para la salida de datos del usuario, que hereda de la clase inicial y agrega el campo de ID y activo
class usuarioSalida(usuarioInicial):
    usuario_id: int = Field(..., description="ID del usuario")
    activo: bool = Field(..., description="Indica si el usuario está activo")
    model_config = ConfigDict(from_attributes=True)
    
#Creamos una clase para la actualización de datos del usuario, que solo permite actualizar el campo de activo
class usuarioActualizar(BaseModel):
    activo: bool = Field(..., description="Indica si el usuario está activo")

# Esquema para el login del usuario, solo con username y password
class LoginRequest(BaseModel):
    username: str
    password: str 