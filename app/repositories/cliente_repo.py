from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.models import ClienteModel, UsuarioModel
from app.repositories.base_repo import BaseRepository

class ClienteRepository(BaseRepository[ClienteModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ClienteModel, db)

    async def get_by_usuario_id(self, usuario_id: int) -> Optional[ClienteModel]:
        stmt = select(ClienteModel).where(ClienteModel.usuario_id == usuario_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    async def count_by_status(self, activo: bool) -> int:
        stmt = select(func.count(ClienteModel.cliente_id)).where(ClienteModel.activo == activo) # Cuenta el número de clientes con el estado especificado
        result = await self.db.execute(stmt)
        return result.scalar() or 0
    async def get_by_status(self, activo: bool, skip: int = 0, limit: int = 100) -> list[ClienteModel]:
        stmt = select(ClienteModel).where(ClienteModel.activo == activo).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def get_by_cedula(self, cedula: str) -> Optional[ClienteModel]:
        stmt = select(ClienteModel).join(UsuarioModel).where(UsuarioModel.cedula == cedula).options(selectinload(ClienteModel.membresias))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()