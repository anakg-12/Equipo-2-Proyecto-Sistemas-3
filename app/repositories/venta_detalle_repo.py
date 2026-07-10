from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import VentaDetalleModel
from app.repositories.base_repo import BaseRepository
from sqlalchemy import insert 

class VentaDetalleRepository(BaseRepository[VentaDetalleModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(VentaDetalleModel, db)

        # Aquí sí va nuestra sobrescritura del método create
    async def create(self, **kwargs) -> VentaDetalleModel:
        """
        Sobrescribimos el create usando SQLAlchemy Core para evitar enviar 
        valores nulos a la columna generada 'subtotal' en PostgreSQL.
        """
        stmt = insert(VentaDetalleModel).values(**kwargs).returning(VentaDetalleModel)
        
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.scalar_one()

    async def get_by_venta(self, venta_id: int) -> List[VentaDetalleModel]:
        stmt = select(VentaDetalleModel).where(VentaDetalleModel.venta_id == venta_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()