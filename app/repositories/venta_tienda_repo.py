from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import VentaTiendaModel
from app.repositories.base_repo import BaseRepository
from datetime import datetime

class VentaTiendaRepository(BaseRepository[VentaTiendaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(VentaTiendaModel, db)

    async def get_by_cliente(self, cliente_id: int) -> List[VentaTiendaModel]:
        stmt = select(VentaTiendaModel).where(VentaTiendaModel.cliente_id == cliente_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_all_with_filters(
        self,
        cliente_id: Optional[int] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[int, List[VentaTiendaModel]]:
        stmt = select(VentaTiendaModel)
        if cliente_id:
            stmt = stmt.where(VentaTiendaModel.cliente_id == cliente_id)
        if fecha_desde:
            stmt = stmt.where(VentaTiendaModel.fecha_venta >= fecha_desde)
        if fecha_hasta:
            stmt = stmt.where(VentaTiendaModel.fecha_venta <= fecha_hasta)
        # Total
        count_stmt = select(func.count()).select_from(VentaTiendaModel)
        if cliente_id:
            count_stmt = count_stmt.where(VentaTiendaModel.cliente_id == cliente_id)
        if fecha_desde:
            count_stmt = count_stmt.where(VentaTiendaModel.fecha_venta >= fecha_desde)
        if fecha_hasta:
            count_stmt = count_stmt.where(VentaTiendaModel.fecha_venta <= fecha_hasta)
        total = (await self.db.execute(count_stmt)).scalar_one()
        stmt = stmt.order_by(VentaTiendaModel.fecha_venta.desc()).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return total, result.scalars().all()