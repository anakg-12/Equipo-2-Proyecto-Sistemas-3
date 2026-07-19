from app.repositories import ReservaInscripcionRepository, SesionProgramadaRepository
from app.schemas.reserva_inscripcion_schema import (
    reservaInscripcionEntrada,
    reservaInscripcionActualizar,
    reservaInscripcionConSesionSalida,
)
from app.models import ReservaInscripcionModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errores import NotFoundException, AppException, BusinessRuleException
from app.constants import (
    SESSION_PROGRAMADA,
    RESERVATION_ACTIVA,
    RESERVATION_CANCELADA,
)


class ReservaInscripcionService:
    def __init__(self, db: AsyncSession):
        self.reserva_inscripcion_repo = ReservaInscripcionRepository(db)
        self.sesion_programada_repo = SesionProgramadaRepository(db)

    # funcion para crear una reserva de inscripcion
    # funcion para crear una reserva de inscripcion
    async def crear_reserva_inscripcion(
        self, cliente_id: int, schema: reservaInscripcionEntrada
    ) -> ReservaInscripcionModel:
        # Revisamos que la sesion exista
        sesion_existe = await self.sesion_programada_repo.get_by_id_or_fail(
            schema.sesion_id, id_column="sesion_id", entity_name="Sesion Programada"
        )

        # validación de estado: se bloquea si la sesión no está programada
        if sesion_existe.estado != SESSION_PROGRAMADA:
            raise BusinessRuleException(
                detail=f"No se puede reservar cupo en esta sesión porque esta se encuentra '{sesion_existe.estado}'. Solo se admiten reservas en sesiones programadas. ",
                error_code="ESTADO_SESION_INVALIDO",
            )

        reserva_previa = await self.reserva_inscripcion_repo.get_by_filtros(
            schema.sesion_id, cliente_id
        )

        if reserva_previa:
            # Si el registro existe y está activo, bloqueamos
            if reserva_previa.estado == RESERVATION_ACTIVA:
                raise BusinessRuleException(
                    detail="El cliente ya tiene una reserva activa para esta sesión",
                    error_code="RESERVA_EXISTENTE",
                )
            # Si el registro existe pero está "cancelada", la dejamos avanzar a las siguientes validaciones

        # vemos si la clase sigue con cupos disponibles, si no, no se puede reservar
        inscritos = await self.reserva_inscripcion_repo.count_activas_by_sesion(
            schema.sesion_id
        )
        if inscritos >= sesion_existe.cupo_maximo:
            raise AppException(
                detail="La sesión programada ya no tiene cupos disponibles",
                error_code="CUPOS_AGOTADOS",
            )

        # vemos que no haya choque de horarios con otras reservas activas del cliente
        choque_horarios = await self.reserva_inscripcion_repo.exist_reserva_conflicto(
            cliente_id, sesion_existe.fecha_hora_inicio, sesion_existe.fecha_hora_fin
        )
        if choque_horarios:
            raise BusinessRuleException(
                detail="La reserva de inscripción tiene un conflicto de horarios con otra reserva activa del cliente",
                error_code="CONFLICTO_HORARIO",
            )
        # Preparamos la data
        reserva_info = schema.model_dump()
        reserva_info["cliente_id"] = cliente_id
        reserva_info["estado"] = RESERVATION_ACTIVA

        if (
            reserva_info.get("fecha_reserva")
            and reserva_info["fecha_reserva"].tzinfo is not None
        ):
            reserva_info["fecha_reserva"] = reserva_info["fecha_reserva"].replace(
                tzinfo=None
            )

        if reserva_previa and reserva_previa.estado == RESERVATION_CANCELADA:
            datos_actualizar = {"estado": RESERVATION_ACTIVA}
            if "fecha_reserva" in reserva_info:
                datos_actualizar["fecha_reserva"] = reserva_info["fecha_reserva"]
            return await self.reserva_inscripcion_repo.update(
                reserva_previa.reserva_id, data=datos_actualizar, id_column="reserva_id"
            )
        else:
            return await self.reserva_inscripcion_repo.create(**reserva_info)

    # funcion para obtener todos los inscritos a una sesion programada
    # 2. OPTIMIZAMOS EL GET
    async def obtener_inscritos_por_sesion(
        self, sesion_id: int
    ) -> list[reservaInscripcionConSesionSalida]:
        sesion_existe = await self.sesion_programada_repo.get_by_id_or_fail(
            sesion_id, id_column="sesion_id", entity_name="Sesion Programada"
        )

        reservas = await self.reserva_inscripcion_repo.get_inscritos_por_sesion(
            sesion_id
        )

        # Construimos la lista utilizando la instancia del esquema modular
        lista_reservas = []
        for r in reservas:
            lista_reservas.append(
                reservaInscripcionConSesionSalida(
                    reserva_id=r.reserva_id,
                    sesion_id=r.sesion_id,
                    nombre_sesion=sesion_existe.nombre,
                    cliente_id=r.cliente_id,
                    estado=r.estado,
                    fecha_reserva=r.fecha_reserva,
                )
            )
        return lista_reservas

    # 3. OPTIMIZAMOS EL PATCH
    async def actualizar_estado_reserva(
        self, sesion_id: int, cliente_id: int, schema: reservaInscripcionActualizar
    ) -> reservaInscripcionConSesionSalida:
        reserva = await self.reserva_inscripcion_repo.get_by_filtros(
            sesion_id, cliente_id
        )
        if not reserva:
            raise NotFoundException(
                detail="La reserva de inscripción no existe",
                error_code="RESERVA_NOT_FOUND",
            )

        reserva_actualizada = await self.reserva_inscripcion_repo.update(
            reserva.reserva_id, {"estado": schema.estado}, id_column="reserva_id"
        )
        sesion_existe = await self.sesion_programada_repo.get_by_id(
            sesion_id, id_column="sesion_id"
        )

        # Retornamos el objeto Pydantic perfectamente validado
        return reservaInscripcionConSesionSalida(
            reserva_id=reserva_actualizada.reserva_id,
            sesion_id=reserva_actualizada.sesion_id,
            nombre_sesion=sesion_existe.nombre,
            cliente_id=reserva_actualizada.cliente_id,
            estado=reserva_actualizada.estado,
            fecha_reserva=reserva_actualizada.fecha_reserva,
        )

    # funcion para cancelar una reserva de inscripcion, que es una actualización del estado a "cancelada"
    async def cancelar_reserva(self, reserva_id: int):
        reserva = await self.reserva_inscripcion_repo.get_by_id_or_fail(
            reserva_id,
            id_column="reserva_id",
            entity_name="Reserva de Inscripción",
        )
        return await self.reserva_inscripcion_repo.update(
            reserva_id, {"estado": RESERVATION_CANCELADA}, id_column="reserva_id"
        )
