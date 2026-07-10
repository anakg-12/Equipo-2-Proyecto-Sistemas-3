from fastapi import APIRouter, HTTPException, Depends, status
from typing import AsyncGenerator, List, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.bd.database import get_db
from app.core.security import decode_token
from app.models.usuario_model import UsuarioModel
from app.repositories.usuario_repo import UsuarioRepository 
from sqlalchemy.orm import selectinload # Importa la nueva función
from sqlalchemy import select
#aqui deberian importar la logíca de los tokens (jwt)

security = HTTPBearer(auto_error=False)

async def get_current_user(
    token_data: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)):
    if token_data is None:
        raise HTTPException(status_code=401, detail="No se proporcionó token de autenticación")
    
    token = token_data.credentials

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=401, detail="Token mal formado")
    
    repo = UsuarioRepository(db)
    user = await repo.get_by_username(username)
    
    if not user or not user.activo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o inactivo")
    return user

# Dependencia para verificar roles de usuario
def requiere_rol(roles_permitidos: list):
    """
    Dependencia que verifica que el usuario autenticado tenga uno de los roles permitidos.
    Uso: Depends(requiere_rol(["Administracion", "Finanzas"]))
    """
    async def dependency(current_user = Depends(get_current_user)):
        rol_usuario = current_user.rol.nombre if current_user.rol else None
        if rol_usuario not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los roles: {roles_permitidos}"
            )
        return current_user
    return dependency
  