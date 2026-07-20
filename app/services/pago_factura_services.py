from app.repositories import (
    PagoFacturaRepository,
    MembresiaClienteRepository,
    PlanSuscripcionRepository,
)
from app.schemas.pago_factura_schema import pagoFacturaEntrada
from app.models import PagoFacturaModel
from app.core.errores import BusinessRuleException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.services.cliente_service import ClienteService
from app.schemas.cliente_schema import clienteActualizar
from app.constants import MembershipState


class PagoFacturaService:
    def __init__(self, db: AsyncSession, cliente_service: ClienteService):
        self.repo = PagoFacturaRepository(db)
        self.membresia_repo = MembresiaClienteRepository(db)
        self.plan_repo = PlanSuscripcionRepository(db)
        self.cliente_service = cliente_service

    async def create_pago_factura(self, schema: pagoFacturaEntrada) -> PagoFacturaModel:
        # verificamos que tenga un plan de suscripcion activo
        membresia = await self.membresia_repo.get_by_id_or_fail(
            schema.membresia_id, id_column="membresia_id", entity_name="Membresia"
        )
        # ver el plan de suscripcion asociado a la membresia
        plan = await self.plan_repo.get_by_id_or_fail(
            membresia.plan_id, id_column="plan_id", entity_name="Plan de Suscripcion"
        )
        # Vemos los costos
        costo_plan = plan.costo
        if schema.monto < costo_plan:
            raise BusinessRuleException(
                detail="El monto debe ser mayor al costo del plan de suscripcion",
                error_code="MONTO_INVALIDO",
            )
        # vemos la fecha
        hoy = datetime.now().date()
        if (
            membresia.estado == MembershipState.activa.value
            and membresia.fecha_fin
            and membresia.fecha_fin > hoy
        ):
            nueva_fecha_inicial = hoy
            nueva_fecha_fin = membresia.fecha_fin + timedelta(days=plan.duracion_dias)
        else:
            nueva_fecha_inicial = hoy
            nueva_fecha_fin = hoy + timedelta(days=plan.duracion_dias)
        vuelto = schema.monto - costo_plan

        # actualizamos la membresia
        datos_actualizar = {
            "fecha_inicio": nueva_fecha_inicial,
            "fecha_fin": nueva_fecha_fin,
            "estado": MembershipState.activa.value,
        }

        await self.membresia_repo.update(
            membresia.membresia_id, data=datos_actualizar, id_column="membresia_id"
        )
        cliente_id = membresia.cliente_id
        schema_activo = clienteActualizar(activo=True)
        await self.cliente_service.update_estado_cliente(cliente_id, schema_activo)
        # creamos el pago de factura
        pago_info = schema.model_dump()
        pago_info["fecha_pago"] = hoy
        return await self.repo.create(**pago_info), vuelto
