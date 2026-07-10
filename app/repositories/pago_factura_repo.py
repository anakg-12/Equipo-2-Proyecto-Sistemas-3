from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import PagoFacturaModel
from app.repositories.base_repo import BaseRepository

class PagoFacturaRepository(BaseRepository[PagoFacturaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(PagoFacturaModel, db)

    async def get_by_membresia(self, membresia_id: int) -> List[PagoFacturaModel]:
        stmt = select(PagoFacturaModel).where(PagoFacturaModel.membresia_id == membresia_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()