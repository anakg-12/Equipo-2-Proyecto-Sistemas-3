from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import PlanSuscripcionModel
from app.repositories.base_repo import BaseRepository

class PlanSuscripcionRepository(BaseRepository[PlanSuscripcionModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(PlanSuscripcionModel, db)

    async def get_activos(self, skip: int = 0, limit: int = 100) -> List[PlanSuscripcionModel]:
        stmt = select(PlanSuscripcionModel).where(PlanSuscripcionModel.activo == True).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()