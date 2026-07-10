from typing import List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models import ControlAccesoModel
from app.repositories.base_repo import BaseRepository

class ControlAccesoRepository(BaseRepository[ControlAccesoModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ControlAccesoModel, db)

    async def get_by_cliente(self, cliente_id: int) -> List[ControlAccesoModel]:
        stmt = select(ControlAccesoModel).where(ControlAccesoModel.cliente_id == cliente_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_fecha(self, fecha: datetime) -> List[ControlAccesoModel]:
        stmt = select(ControlAccesoModel).where(
            and_(
                ControlAccesoModel.fecha_hora_entrada >= fecha,
                ControlAccesoModel.fecha_hora_entrada < fecha + timedelta(days=1)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()