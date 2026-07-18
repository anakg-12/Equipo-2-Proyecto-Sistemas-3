from app.repositories import PlanSuscripcionRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PlanService:
    def __init__(self, db: AsyncSession):
        self.plan_repo = PlanSuscripcionRepository(db)

    # Hacemos la funcion para listar todos los planes de suscripción
    async def list_planes(self, skip: int = 0, limit: int = 100):
        total = await self.plan_repo.count()
        res = await self.plan_repo.get_all(skip, limit)
        return total, res
