from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import EvaluacionBiometricaModel
from app.repositories.base_repo import BaseRepository

class EvaluacionBiometricaRepository(BaseRepository[EvaluacionBiometricaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(EvaluacionBiometricaModel, db)

    async def get_by_cliente(self, cliente_id: int) -> List[EvaluacionBiometricaModel]:
        stmt = select(EvaluacionBiometricaModel).where(EvaluacionBiometricaModel.cliente_id == cliente_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()