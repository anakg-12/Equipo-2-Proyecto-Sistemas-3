from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models import MembresiaClienteModel
from app.repositories.base_repo import BaseRepository
from app.constants import MembershipState

class MembresiaClienteRepository(BaseRepository[MembresiaClienteModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(MembresiaClienteModel, db)

    async def get_ultima_membresia(self, cliente_id: int) -> Optional[MembresiaClienteModel]:
        stmt = select(MembresiaClienteModel).where(MembresiaClienteModel.cliente_id == cliente_id).order_by(MembresiaClienteModel.fecha_fin.desc()).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_por_cliente(self, cliente_id: int) -> List[MembresiaClienteModel]:
        stmt = select(MembresiaClienteModel).where(MembresiaClienteModel.cliente_id == cliente_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_membresia_activa(self, cliente_id: int) -> Optional[MembresiaClienteModel]:
        hoy = date.today()
        stmt = select(MembresiaClienteModel).where(
            and_(
                MembresiaClienteModel.cliente_id == cliente_id,
                MembresiaClienteModel.fecha_fin >= hoy,
                MembresiaClienteModel.estado == MembershipState.activa.value
            )
        ).order_by(MembresiaClienteModel.fecha_fin.desc()).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none(
        )