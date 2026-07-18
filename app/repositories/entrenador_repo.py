from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import EntrenadorModel, UsuarioModel
from app.repositories.base_repo import BaseRepository

class EntrenadorRepository(BaseRepository[EntrenadorModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(EntrenadorModel, db)

    async def get_by_usuario_id(self, usuario_id: int) -> Optional[EntrenadorModel]:
        stmt = select(EntrenadorModel).where(EntrenadorModel.usuario_id == usuario_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_activos(self, skip: int = 0, limit: int = 100) -> List[EntrenadorModel]:
        stmt = select(EntrenadorModel).where(EntrenadorModel.activo == True).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def get_usuario_by_id(self, usuario_id: int):
        stmt = select(UsuarioModel).options(selectinload(UsuarioModel.rol)).where(UsuarioModel.usuario_id == usuario_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()