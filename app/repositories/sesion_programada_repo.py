from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models import SesionProgramadaModel
from app.repositories.base_repo import BaseRepository

class SesionProgramadaRepository(BaseRepository[SesionProgramadaModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(SesionProgramadaModel, db)
    
    async def get_by_filtros(self, estado: Optional[str] = None, fecha: Optional[date] = None, disciplina_id: Optional[int] = None, entrenador_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[SesionProgramadaModel]:
        stmt = select(SesionProgramadaModel)
        if estado:
            stmt = stmt.where(SesionProgramadaModel.estado == estado)
        if fecha:
            stmt = stmt.where(func.date(SesionProgramadaModel.fecha_hora_inicio) == fecha)
        if entrenador_id:
            stmt = stmt.where(SesionProgramadaModel.entrenador_id == entrenador_id)
        if disciplina_id:
            stmt = stmt.where(SesionProgramadaModel.disciplina_id == disciplina_id)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def count_by_filtros(self, estado: Optional[str] = None, fecha: Optional[date] = None, disciplina_id: Optional[int] = None, entrenador_id: Optional[int] = None) -> int:
        stmt = select(func.count(SesionProgramadaModel.sesion_id))
        if estado:
            stmt = stmt.where(SesionProgramadaModel.estado == estado)
        if fecha:
            stmt = stmt.where(func.date(SesionProgramadaModel.fecha_hora_inicio) == fecha)
        if entrenador_id:
            stmt = stmt.where(SesionProgramadaModel.entrenador_id == entrenador_id)
        if disciplina_id:
            stmt = stmt.where(SesionProgramadaModel.disciplina_id == disciplina_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0
    

    
    async def count_sesion(self, **kwargs):
        stmt = select(func.count()).select_from(self.model)
        
        if "fecha_hora_inicio" in kwargs and kwargs["fecha_hora_inicio"] is not None:
            fecha_filtro = kwargs.pop("fecha_hora_inicio") 
            stmt = stmt.where(func.date(self.model.fecha_hora_inicio) == fecha_filtro)
        
        stmt = stmt.filter_by(**kwargs)
        
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_all_sesion(self, skip: int = 0, limit: int = 100, **kwargs):
        stmt = select(self.model)
        if "fecha_hora_inicio" in kwargs and kwargs["fecha_hora_inicio"] is not None:
            fecha_filtro = kwargs.pop("fecha_hora_inicio")
            stmt = stmt.where(func.date(self.model.fecha_hora_inicio) == fecha_filtro)
            
        stmt = stmt.filter_by(**kwargs).offset(skip).limit(limit)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
