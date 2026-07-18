from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import UsuarioModel
from app.repositories.base_repo import BaseRepository
from sqlalchemy.orm import selectinload
from sqlalchemy import select

class UsuarioRepository(BaseRepository[UsuarioModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(UsuarioModel, db)

    async def get_by_email(self, email: str, id_column: str = "email") -> Optional[UsuarioModel]:
        stmt = select(UsuarioModel).where(getattr(UsuarioModel, id_column) == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_cedula(self, cedula: str, id_column: str = "cedula") -> Optional[UsuarioModel]:
        stmt = select(UsuarioModel).where(getattr(UsuarioModel, id_column) == cedula)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str, id_column: str = "username") -> Optional[UsuarioModel]:
        stmt = select(UsuarioModel).where(getattr(UsuarioModel, id_column) == username).options(selectinload(UsuarioModel.rol))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_activos(self, skip: int = 0, limit: int = 100) -> List[UsuarioModel]:
        stmt = select(UsuarioModel).where(UsuarioModel.activo == True).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id_with_rol(self, usuario_id: int):
        stmt = select(UsuarioModel).options(selectinload(UsuarioModel.rol)).where(UsuarioModel.usuario_id == usuario_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()