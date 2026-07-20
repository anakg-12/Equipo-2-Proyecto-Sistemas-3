from app.repositories import ControlAccesoRepository, ClienteRepository
from app.models import ControlAccesoModel
from app.schemas.control_acceso_schema import controlAccesoEntrada
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from app.core.exceptions import AppException
from app.core.errores import NotFoundException
from app.constants import MembershipState


class ControlAccesoService:
    def __init__(self, db: AsyncSession):
        self.repo = ControlAccesoRepository(db)
        self.cliente_repo = ClienteRepository(db)

    # Esta función registra la entrada del cliente y valida su membresía.
    async def registrar_y_validar_entrada(
        self, schema: controlAccesoEntrada
    ) -> ControlAccesoModel:
        # Hay que buscar al cliente por su cedula
        cliente_existente = await self.cliente_repo.get_by_cedula(schema.cedula)
        if not cliente_existente:
            raise NotFoundException(
                detail="Cliente no encontrado", error_code="CLIENTE_NOT_FOUND"
            )

        if not cliente_existente.activo:
            raise AppException(
                detail="El cliente está inactivo. Acceso denegado.",
                error_code="CLIENTE_INACTIVO",
                status_code=403,
            )
        hoy = date.today()
        membresia_valida = False

        for membresia in cliente_existente.membresias:
            if (
                membresia.estado in [MembershipState.activa.value, MembershipState.por_vencer.value]
                and membresia.fecha_inicio <= hoy <= membresia.fecha_fin
            ):
                membresia_valida = True
                break
        if not membresia_valida:
            raise AppException(
                detail="Membresía no válida para acceso",
                error_code="MEMBRESIA_INVALIDA",
                status_code=403,
            )
        acceso_info = {
            "cliente_id": cliente_existente.cliente_id,
            "fecha_hora_entrada": datetime.now(),
            "observaciones": schema.observaciones,
        }
        acceso = await self.repo.create(**acceso_info)
        return acceso
