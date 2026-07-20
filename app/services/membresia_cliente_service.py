from app.repositories import (
    MembresiaClienteRepository,
    ClienteRepository,
    PlanSuscripcionRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.core.errores import AppException
from app.models import MembresiaClienteModel
from app.schemas.membresia_cliente_schema import membresiaClienteCrear
from app.constants import MembershipState


class MembresiaClienteService:
    def __init__(self, db: AsyncSession):
        self.membresia_repo = MembresiaClienteRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.plan_repo = PlanSuscripcionRepository(db)

    # Metodo para saber el estado de una membresia
    async def saber_estado_membresia(self, cliente_id: int) -> dict:
        # vemos si el cliente existe
        cliente_existe = await self.cliente_repo.get_by_id_or_fail(
            cliente_id, id_column="cliente_id", entity_name="Cliente"
        )
        # vemos si el cliente esta activo
        if not cliente_existe.activo:
            return {
                "cliente_id": cliente_id,
                "estado": MembershipState.inactiva.value,
                "mensaje": "El cliente no está activo en el sistema.",
            }
        # vemos si el cliente tiene una membresia activa
        membresia_existe = await self.membresia_repo.get_ultima_membresia(cliente_id)
        if not membresia_existe:
            return {"cliente_id": cliente_id, "estado": MembershipState.ninguna.value}

        dia_hoy = datetime.now().date()
        fecha_final = membresia_existe.fecha_fin
        dias_que_quedan = (fecha_final - dia_hoy).days
        if dias_que_quedan <= 0:
            estado = MembershipState.vencida.value
        elif 3 >= dias_que_quedan > 0:
            estado = MembershipState.por_vencer.value
        else:
            estado = MembershipState.activa.value
        return {
            "cliente_id": cliente_id,
            "estado": estado,
            "dias_restantes": max(0, dias_que_quedan),
            "membresia_id": membresia_existe.membresia_id,
            "plan_id": membresia_existe.plan_id,
            "fecha_inicio": membresia_existe.fecha_inicio,
            "fecha_fin": membresia_existe.fecha_fin,
        }

    # Crear una membresia para un cliente
    async def crear_membresia_cliente(
        self, schema: membresiaClienteCrear
    ) -> MembresiaClienteModel:

        # vemos si el cliente existe
        cliente_existe = await self.cliente_repo.get_by_id_or_fail(
            schema.cliente_id, id_column="cliente_id", entity_name="Cliente"
        )

        # vemos si el cliente ya tiene una membresia activa
        membresia_activa = await self.membresia_repo.get_membresia_activa(
            cliente_id=schema.cliente_id
        )
        if membresia_activa:
            raise AppException(
                detail="El cliente ya tiene una membresía activa, no se puede crear otra membresía hasta que la actual expire.",
                error_code="MEMBRESIA_ACTIVA_EXISTENTE",
                status_code=400,
            )
        # vemos si existe el plan de suscripcion
        plan_existe = await self.plan_repo.get_by_id_or_fail(
            schema.plan_id, id_column="plan_id", entity_name="Plan"
        )
        # calculamos la fecha de fin de la membresia
        fecha_inicio = (
            schema.fecha_inicio if schema.fecha_inicio else datetime.now().date()
        )
        fecha_fin = fecha_inicio + timedelta(days=plan_existe.duracion_dias)

        # si todo esta bien, creamos la membresia para el cliente
        membresia_info = schema.model_dump()
        membresia_info["fecha_inicio"] = fecha_inicio
        membresia_info["fecha_fin"] = fecha_fin
        membresia_info["estado"] = MembershipState.inactiva.value  # La membresía se crea como inactiva por defecto, se activará al realizar el pago
        return await self.membresia_repo.create(**membresia_info)
