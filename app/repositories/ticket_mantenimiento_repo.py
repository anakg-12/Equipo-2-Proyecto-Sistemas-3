from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import TicketMantenimientoModel, UsuarioModel
from app.repositories.base_repo import BaseRepository

class TicketMantenimientoRepository(BaseRepository[TicketMantenimientoModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(TicketMantenimientoModel, db)

    async def get_by_maquina(self, maquina_id: int) -> List[TicketMantenimientoModel]:
        stmt = select(TicketMantenimientoModel).where(TicketMantenimientoModel.maquina_id == maquina_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_abiertos(self) -> List[TicketMantenimientoModel]:
        stmt = select(TicketMantenimientoModel).where(TicketMantenimientoModel.estado == "abierto")
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def verificar_usuario_admin(self, usuario_id: int) -> bool:
        stmt = select(UsuarioModel).where(UsuarioModel.usuario_id == usuario_id)
        result = await self.db.execute(stmt)
        usuario = result.scalar_one_or_none()
        if usuario and usuario.rol_id == 1:  # Asumiendo que el rol de administrador tiene ID 1
            return True
        return False
    
    async def exist_ticket_abierto(self, maquina_id: int) -> bool:
        stmt = select(TicketMantenimientoModel).where(
            TicketMantenimientoModel.maquina_id == maquina_id,
            TicketMantenimientoModel.estado == "abierto"
        )
        result = await self.db.execute(stmt)
        ticket = result.scalar_one_or_none()
        return ticket is not None