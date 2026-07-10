from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ProductoTiendaModel
from app.repositories.base_repo import BaseRepository
from typing import List, Optional, Tuple
from sqlalchemy import select, func

class ProductoTiendaRepository(BaseRepository[ProductoTiendaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductoTiendaModel, db)

    async def get_all_paginated(
        self,
        categoria: Optional[str] = None,
        stock_min: Optional[int] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[int, List[ProductoTiendaModel]]:
        stmt = select(ProductoTiendaModel)
        if categoria:
            stmt = stmt.where(ProductoTiendaModel.categoria == categoria)
        if stock_min is not None:
            stmt = stmt.where(ProductoTiendaModel.stock >= stock_min)
        # Total
        count_stmt = select(func.count()).select_from(ProductoTiendaModel)
        if categoria:
            count_stmt = count_stmt.where(ProductoTiendaModel.categoria == categoria)
        if stock_min is not None:
            count_stmt = count_stmt.where(ProductoTiendaModel.stock >= stock_min)
        total = (await self.db.execute(count_stmt)).scalar_one()
        # Paginado
        stmt = stmt.order_by(ProductoTiendaModel.producto_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return total, result.scalars().all()

    async def update_stock(self, producto_id: int, nuevo_stock: int) -> None:
        await self.update(producto_id, {"stock": nuevo_stock}, id_column="producto_id")