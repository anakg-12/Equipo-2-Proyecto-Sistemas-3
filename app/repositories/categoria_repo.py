from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CategoriaMaquinaModel
from app.repositories.base_repo import BaseRepository

class CategoriaRepository(BaseRepository[CategoriaMaquinaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(CategoriaMaquinaModel, db)

    async def get_by_nombre(self, nombre: str) -> CategoriaMaquinaModel:
        stmt = select(CategoriaMaquinaModel).where(func.lower(CategoriaMaquinaModel.nombre) == nombre.lower())
        result = await self.db.execute(stmt)
        return result.scalars().first()