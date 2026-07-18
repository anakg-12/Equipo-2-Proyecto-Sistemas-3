from app.repositories import EvaluacionBiometricaRepository, ClienteRepository
from app.models import EvaluacionBiometricaModel
from app.schemas.evaluacion_biometrica_schema import EvaluacionBiometricaCrear
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple
from datetime import date


class EvaluacionBiometricaService:
    def __init__(self, db: AsyncSession):
        self.evaluacion_repo = EvaluacionBiometricaRepository(db)
        self.cliente_repo = ClienteRepository(db)

    async def crear_evaluacion(
        self, cliente_id: int, schema: EvaluacionBiometricaCrear
    ) -> EvaluacionBiometricaModel:
        cliente = await self.cliente_repo.get_by_id_or_fail(
            cliente_id, id_column="cliente_id", entity_name="Cliente"
        )
        evaluacion_info = schema.model_dump()
        evaluacion_info["cliente_id"] = cliente_id
        if evaluacion_info.get("fecha") is None:
            evaluacion_info["fecha"] = date.today()
        return await self.evaluacion_repo.create(**evaluacion_info)

    async def listar_evaluaciones(
        self, cliente_id: int, skip: int = 0, limit: int = 100
    ) -> Tuple[int, List[EvaluacionBiometricaModel]]:
        cliente = await self.cliente_repo.get_by_id_or_fail(
            cliente_id, id_column="cliente_id", entity_name="Cliente"
        )
        total = await self.evaluacion_repo.count(cliente_id=cliente_id)
        evaluaciones = await self.evaluacion_repo.get_all(
            skip=skip, limit=limit, cliente_id=cliente_id
        )
        return total, evaluaciones
