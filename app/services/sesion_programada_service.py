from datetime import date

from app.repositories import (
    SesionProgramadaRepository,
    UsuarioRepository,
    EntrenadorRepository,
    ReservaInscripcionRepository,
)
from app.models import SesionProgramadaModel
from app.schemas.sesion_programada_schema import (
    sesionProgramadaEntrada,
    sesionProgramadaActualizar,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class SesionProgramadaService:
    def __init__(self, db: AsyncSession):
        self.sesion_programada = SesionProgramadaRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.entrenador_repo = EntrenadorRepository(db)
        self.reserva_repo = ReservaInscripcionRepository(db)

    # hacemos una funcion para el filtrado con fecha, nombre, paginacion y estado activa
    async def list_sesiones(
        self,
        estado: Optional[str] = None,
        fecha: Optional[date] = None,
        disciplina_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ):
        if disciplina_id is not None:
            filtros = {"disciplina_id": disciplina_id}
            if estado is not None:
                filtros["estado"] = estado
            if fecha is not None:
                filtros["fecha_hora_inicio"] = fecha
            total = await self.sesion_programada.count_sesion(**filtros)
            sesiones = await self.sesion_programada.get_all_sesion(
                skip=skip, limit=limit, **filtros
            )
        elif estado is not None or fecha is not None:
            filtros = {}
            if estado is not None:
                filtros["estado"] = estado
            if fecha is not None:
                filtros["fecha_hora_inicio"] = fecha
            total = await self.sesion_programada.count_sesion(**filtros)
            sesiones = await self.sesion_programada.get_all_sesion(
                skip=skip, limit=limit, **filtros
            )
        else:
            total = await self.sesion_programada.count()
            sesiones = await self.sesion_programada.get_all(skip=skip, limit=limit)
        return total, sesiones

    # se crea una nueva sesion programada y se busca validar que el entrenador no tenga otra clase a la misma hora
    async def create_sesion(
        self, schema: sesionProgramadaEntrada
    ) -> SesionProgramadaModel:
        # Limpiar la zona horaria para que asyncpg y PostgreSQL no se quejen
        schema.fecha_hora_inicio = schema.fecha_hora_inicio.replace(tzinfo=None)
        schema.fecha_hora_fin = schema.fecha_hora_fin.replace(tzinfo=None)
        sesion_info = schema.model_dump()
        sesion_info["estado"] = (
            "programada"  # al crearla se debe colocar para postgresql que esta programada la sesion
        )
        return await self.sesion_programada.create(**sesion_info)

    # funcion para cambiar el estado de una sesion programada
    async def update_sesion_estado(
        self, sesion_id: int, schema: sesionProgramadaActualizar
    ) -> SesionProgramadaModel:
        sesion_existente = await self.sesion_programada.get_by_id_or_fail(
            sesion_id, id_column="sesion_id", entity_name="Sesion Programada"
        )

        nuevo_estado = schema.estado.value
        actualizar_info = {"estado": nuevo_estado}

        sesion_actualizada = await self.sesion_programada.update(
            id=sesion_id, data=actualizar_info, id_column="sesion_id"
        )

        if nuevo_estado == "cancelada":
            await self.reserva_repo.cancelar_reservas_por_sesion(sesion_id)

        return sesion_actualizada

    # funcion que permite que los entrenadores puedan ver las clases programadas donde ellos se encuentren
    async def listar_sesiones_usuario(
        self, usuario_id: int, page: int = 1, limit: int = 100
    ):
        entrenador = await self.entrenador_repo.get_by_usuario_id_or_fail(
            usuario_id, id_column="usuario_id", entity_name="Entrenador"
        )
        skip = (page - 1) * limit
        total = await self.sesion_programada.count_by_filtros(
            entrenador_id=entrenador.entrenador_id
        )
        sesiones = await self.sesion_programada.get_by_filtros(
            entrenador_id=entrenador.entrenador_id, skip=skip, limit=limit
        )
        return total, sesiones
