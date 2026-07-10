from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import MaquinaModel
from app.repositories.base_repo import BaseRepository
from sqlalchemy import func

class MaquinaRepository(BaseRepository[MaquinaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(MaquinaModel, db)

    async def get_by_categoria(self, categoria_id: int, skip: int = 0, limit: int = 100) -> List[MaquinaModel]:
        stmt = select(MaquinaModel).where(MaquinaModel.categoria_id == categoria_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_estado(self, estado: str) -> List[MaquinaModel]:
        stmt = select(MaquinaModel).where(MaquinaModel.estado_operativo == estado)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def count_by_categoria(self, categoria_id: int) -> int:
        stmt = select(func.count(MaquinaModel.maquina_id)).where(MaquinaModel.categoria_id == categoria_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0