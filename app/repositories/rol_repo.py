from sqlalchemy.ext.asyncio import AsyncSession
from app.models import RolModel
from app.repositories.base_repo import BaseRepository

class RolRepository(BaseRepository[RolModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(RolModel, db)