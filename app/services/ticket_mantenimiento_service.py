from datetime import datetime

from app.repositories import TicketMantenimientoRepository, MaquinaRepository
from app.models import TicketMantenimientoModel
from app.schemas.ticket_mantenimiento_schema import (
    ticketMantenimientoCrear,
    ticketMantenimientoActualizar,
    ticketMantenimientoResolver,
)
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errores import NotFoundException, AppException
from app.constants import TicketState, MachineStatus


class TicketMantenimientoService:
    def __init__(self, db: AsyncSession):
        self.ticket_repo = TicketMantenimientoRepository(db)
        self.maquina_repo = MaquinaRepository(db)

    async def crear_ticket_y_actualizar_maquina(
        self, maquina_id: int, schema: ticketMantenimientoCrear
    ) -> TicketMantenimientoModel:
        # vemos si la maquina existe
        maquina = await self.maquina_repo.get_by_id_or_fail(maquina_id, id_column="maquina_id", entity_name="Maquina")
        # vemos si el usuario que reporta el problema es un administrador, si no, no se puede crear el ticket de mantenimiento
        es_admin = await self.ticket_repo.verificar_usuario_admin(schema.reportado_por)
        if not es_admin:
            raise NotFoundException(
                detail="El usuario que reporta el problema no es un administrador",
                error_code="USUARIO_NO_ADMIN",
            )
        # vemos si ya hay un ticket abierto para esa maquina, si es asi, no se puede crear otro ticket de mantenimiento hasta que se cierre el ticket abierto
        tickets_abiertos = await self.ticket_repo.exist_ticket_abierto(maquina_id)
        if tickets_abiertos:
            raise AppException(
                detail="Ya hay un ticket abierto para esta maquina",
                error_code="TICKET_ABERTO",
                status_code=400,
            )
        # creamos el ticket de mantenimiento y actualizamos el estado de la maquina a "en mantenimiento"
        ticket_info = schema.model_dump()
        ticket_info["maquina_id"] = maquina_id
        ticket_info["estado"] = TicketState.abierto.value
        ticket_info["fecha_reporte"] = datetime.now()
        await self.maquina_repo.update(
            id=maquina_id,
            data={"estado_operativo": MachineStatus.en_mantenimiento.value},
            id_column="maquina_id",
        )
        return await self.ticket_repo.create(**ticket_info)

    # funcion para listar los tickets abiertos
    async def list_tickets_maquina(
        self, maquina_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> Tuple[int, List[TicketMantenimientoModel]]:

        if maquina_id is not None:
            # vemos si la maquina existe
            existe_maquina = await self.maquina_repo.get_by_id_or_fail(
                maquina_id, id_column="maquina_id", entity_name="Maquina"
            )
            # vemos si hay tickets abiertos para esa maquina
            total = await self.ticket_repo.count(maquina_id=maquina_id)
            tickets = await self.ticket_repo.get_all(
                maquina_id=maquina_id, skip=skip, limit=limit
            )
        else:
            # obtenemos todos los tickets abiertos
            total = await self.ticket_repo.count()
            tickets = await self.ticket_repo.get_all(skip=skip, limit=limit)
        return total, tickets

    async def actualizar_ticket(
        self, ticket_id: int, schema: ticketMantenimientoActualizar
    ) -> TicketMantenimientoModel:
        # vemos si el ticket existe
        ticket_existente = await self.ticket_repo.get_by_id_or_fail(
            ticket_id, id_column="ticket_id", entity_name="Ticket de Mantenimiento"
        )
        # actualizamos el ticket de mantenimiento
        ticket_existente.estado = schema.estado.value
        return await self.ticket_repo.update(
            id=ticket_id,
            data={"estado": ticket_existente.estado},
            id_column="ticket_id",
        )

    async def resolver_ticket(
        self, ticket_id: int, schema: ticketMantenimientoResolver
    ) -> TicketMantenimientoModel:
        ticket_existente = await self.ticket_repo.get_by_id_or_fail(
            ticket_id, id_column="ticket_id", entity_name="Ticket de Mantenimiento"
        )
        # actualizamos el estado de la maquina a "activa"
        maquina = await self.maquina_repo.get_by_id(
            ticket_existente.maquina_id, id_column="maquina_id"
        )
        if maquina:
            await self.maquina_repo.update(
                id=maquina.maquina_id,
                data={"estado_operativo": MachineStatus.activa.value},
                id_column="maquina_id",
            )
        # corregimos la fecha de resolucion
        fecha_limpia = schema.fecha_resolucion.replace(tzinfo=None)
        ticket_info = {
            "estado": TicketState.cerrado.value,
            "fecha_resolucion": fecha_limpia,
            "costo_reparacion": schema.costo_reparacion,
        }
        return await self.ticket_repo.update(
            id=ticket_id, data=ticket_info, id_column="ticket_id"
        )
