from app.repositories import EntrenadorRepository
from app.repositories.usuario_repo import UsuarioRepository
from app.schemas.entrenador_schema import entrenadorActualizar, entrenadorInicial
from app.models import EntrenadorModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errores import NotFoundException

class entrenadorService:
    def __init__(self, db: AsyncSession):
        self.entrenador_repo = EntrenadorRepository(db)
        self.usuario_repo = UsuarioRepository(db)
    #Funcion para crear un entrenador nuevo
    async def create_entrenador(self, schema: entrenadorInicial) -> EntrenadorModel:
        # verificamos que exista el id del usuario
        usuario = await self.entrenador_repo.get_usuario_by_id(schema.usuario_id)
        if not usuario:
            raise NotFoundException(detail="Id de Usuario no encontrado", error_code="ID_NOT_FOUND")
        #verificamos que el usuario sea un entrenador por la id
        if usuario.rol_id != 3:  
            raise NotFoundException(detail="El usuario no tiene el rol de entrenador", error_code="USER_NOT_TRAINER_ROLE")
        entrenador_info = schema.model_dump()
        entrenador_info["activo"] = True
        return await self.entrenador_repo.create(**entrenador_info)

    #Creamos la función para cambiar el estado del entrenador
    async def update_estado_entrenador(self, id: int, schema: entrenadorActualizar) -> EntrenadorModel:
        entrenador_existente = await self.entrenador_repo.get_by_id(id, id_column="entrenador_id")
        if not entrenador_existente:
            raise NotFoundException(detail="Id de Entrenador no encontrado", error_code="ID_NOT_FOUND")
        actualizar_info = schema.model_dump(exclude_unset=True)
        nuevo_estado = actualizar_info.get("activo")

        entrenador_actualizado = await self.entrenador_repo.update(entrenador_existente.entrenador_id, actualizar_info, id_column="entrenador_id")
        if nuevo_estado is not None:
            usuario_repo = UsuarioRepository(self.entrenador_repo.db)
            await usuario_repo.update(entrenador_existente.usuario_id, {"activo": nuevo_estado}, id_column="usuario_id")
        return entrenador_actualizado
    