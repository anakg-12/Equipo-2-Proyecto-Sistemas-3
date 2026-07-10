from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import requiere_rol
from app.bd.database import get_db
from app.schemas.response import StandardResponse, PaginatedResponse

from app.schemas.usuario_schema import (
    usuarioEntrada,
    usuarioSalida,
    usuarioActualizar,
    UsuarioFiltros,
    LoginRequest
)
from app.services.usuario_service import UsuarioService
from app.core.security import create_access_token

router = APIRouter(prefix="/api/v1",
                    tags=["Autenticación y Gestión de Usuarios"])

def get_usuario_service(db: AsyncSession = Depends(get_db)) -> UsuarioService:
    return UsuarioService(db)

@router.post("/auth/login", status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest,
    service: UsuarioService = Depends(get_usuario_service)
):  
    
    """
    Auténtico usuario y retorna el JWT. 
    Accesible para todos.
    """

    # Autenticación: esperamos que el servicio valide y retorne el usuario
    user = await service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Crear token con el username
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"} 

#--- endpoints solo para Administración ---#

@router.post("/usuarios", 
             status_code=status.HTTP_201_CREATED, 
             response_model=StandardResponse[usuarioSalida],
             dependencies=[Depends(requiere_rol("Administracion"))])
async def registrar_usuario(
    schema: usuarioEntrada,
    service: UsuarioService = Depends(get_usuario_service)
):
    """Registro de usuario nuevos, solo para Administración"""
    res = await service.create_usuario(schema)
    return {
        "status": "success",
        "message": "Usuario registrado exitosamente",
        "data": res
    }


@router.patch("/usuarios/{id}/estado", 
              dependencies=[Depends(requiere_rol("Administracion"))])
async def cambiar_estado_usuario(
    id: int, 
    schema: usuarioActualizar,
    service: UsuarioService = Depends(get_usuario_service)
):
    """Permite actualizar el estado (activar o desactivar) de una cuenta.
    Accesible de para Administración.
    """
    res = await service.update_estado_usuario(id, schema)
    return {
        "status": "success",
        "message": "Estado de usuario actualizado",
        "data": res
    }

@router.get("/usuarios", 
            response_model=PaginatedResponse[usuarioSalida],
            dependencies=[Depends(requiere_rol("Administracion"))])
async def listar_usuarios(
    filtros: UsuarioFiltros = Depends(), 
    service: UsuarioService = Depends(get_usuario_service)
):
    """Lista todos los usuarios. Soporta el filtro opcional por ID y paginación.
    Accesible solo para Administración.
    """
    
    # Calculamos el salto para la base de datos
    skip = (filtros.page - 1) * filtros.limit
    
    total, res = await service.list_usuarios(
        usuario_id=filtros.usuario_id,
        skip=skip,
        limit=filtros.limit
    )
    if total == 1:
        return {
            "status": "success",
            "message": "Usuario obtenido exitosamente",
            "data": res,
            "total": total,
            "page": filtros.page,
            "limit": filtros.limit
        }
    return {
        "status": "success",
        "message": "Usuarios obtenidos exitosamente",
        "data": res,
        "total": total,
        "page": filtros.page,
        "limit": filtros.limit
    }