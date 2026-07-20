from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload
from app.models import ReservaInscripcionModel, SesionProgramadaModel
from app.repositories.base_repo import BaseRepository
from datetime import datetime
from app.constants import ReservationState

class ReservaInscripcionRepository(BaseRepository[ReservaInscripcionModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ReservaInscripcionModel, db)

    async def get_activas_by_cliente(self, cliente_id: int) -> List[ReservaInscripcionModel]:
        stmt = select(ReservaInscripcionModel).where(
            ReservaInscripcionModel.cliente_id == cliente_id,
            ReservaInscripcionModel.estado == ReservationState.activa.value
        ).options(selectinload(ReservaInscripcionModel.sesion))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def count_activas_by_sesion(self, sesion_id: int) -> int:
        stmt = select(func.count()).select_from(ReservaInscripcionModel).where(
            ReservaInscripcionModel.sesion_id == sesion_id,
            ReservaInscripcionModel.estado == ReservationState.activa.value
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()
    
    async def exist_reserva(self, cliente_id: int, sesion_id: int) -> bool:
        stmt = select(func.count()).select_from(ReservaInscripcionModel).where(
            ReservaInscripcionModel.cliente_id == cliente_id,
            ReservaInscripcionModel.sesion_id == sesion_id,
            ReservaInscripcionModel.estado == ReservationState.activa.value
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() > 0
    async def exist_reserva_conflicto(self, cliente_id: int, fecha_inicio: datetime, fecha_fin: datetime) -> bool:
        stmt = select(func.count()).select_from(ReservaInscripcionModel).join(
            SesionProgramadaModel
        ).where(
            ReservaInscripcionModel.cliente_id == cliente_id,
            ReservaInscripcionModel.estado == ReservationState.activa.value,
            SesionProgramadaModel.fecha_hora_inicio < fecha_fin,
            SesionProgramadaModel.fecha_hora_fin > fecha_inicio
            )
        
        result = await self.db.execute(stmt)
        return result.scalar_one() > 0
    async def get_inscritos_por_sesion(self, sesion_id: int) -> List[ReservaInscripcionModel]:
        stmt = select(ReservaInscripcionModel).where(
            ReservaInscripcionModel.sesion_id == sesion_id,
            ReservaInscripcionModel.estado == ReservationState.activa.value
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def get_by_filtros(self, sesion_id: int, cliente_id: int) -> ReservaInscripcionModel:
        stmt = select(ReservaInscripcionModel).where(
            ReservaInscripcionModel.sesion_id == sesion_id,
            ReservaInscripcionModel.cliente_id == cliente_id,
        ).order_by(ReservaInscripcionModel.fecha_reserva.desc()).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def cancelar_reservas_por_sesion(self, sesion_id: int) -> None:
        """
        Actualiza masivamente a 'cancelada' todas las reservas activas 
        que pertenezcan a una sesión específica.
        """
        stmt = (
            update(ReservaInscripcionModel)
            .where(
                ReservaInscripcionModel.sesion_id == sesion_id,
                ReservaInscripcionModel.estado == ReservationState.activa.value
            )
            .values(estado=ReservationState.cancelada.value)
        )
        await self.db.execute(stmt)
        await self.db.commit()