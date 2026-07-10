from sqlalchemy.ext.asyncio import AsyncSession
from app.models import DisciplinaModel
from app.repositories.base_repo import BaseRepository

class DisciplinaRepository(BaseRepository[DisciplinaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(DisciplinaModel, db)