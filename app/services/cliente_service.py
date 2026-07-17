from app.models.usuario_model import UsuarioModel
from app.repositories import ClienteRepository, UsuarioRepository
from app.schemas.cliente_schema import clienteActualizar, clienteInicial
from app.models import ClienteModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.errores import NotFoundException, AppException
from typing import Optional
from fastapi import Depends
from app.dependencies import get_current_user
from app.models.rol_model import RolesEnum

class ClienteService:
    def __init__(self, db: AsyncSession):
        self.repo = ClienteRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    # Funcion para crear un cliente nuevo
    async def create_cliente(self, schema: clienteInicial) -> ClienteModel:
        # verificamos que exista el id del usuario
        usuario = await self.usuario_repo.get_by_id_with_rol(schema.usuario_id)
        if not usuario:
            raise NotFoundException(detail="Id de Usuario no encontrado", error_code="ID_NOT_FOUND")
        # verificamos que el usuario sea un cliente por el nombre del rol
        if not usuario.rol or usuario.rol.nombre != RolesEnum.CLIENTES:
            raise AppException(detail="El usuario no tiene el rol de cliente", error_code="USER_NOT_CLIENT_ROLE", status_code=400)
        cliente_info = schema.model_dump()
        cliente_info["activo"] = False  # El cliente se crea como inactivo por defecto
        return await self.repo.create(**cliente_info)

    # funcion para actualizar el estado del cliente
    async def update_estado_cliente(self, cliente_id: int, schema: clienteActualizar) -> ClienteModel:
        cliente = await self.repo.get_by_id(cliente_id, id_column="cliente_id")
        if not cliente:
            raise NotFoundException(detail="Id de Cliente no encontrado", error_code="ID_NOT_FOUND")
        nuevo_estado = schema.activo
        cliente_actualizado = await self.repo.update(cliente_id, {"activo": nuevo_estado}, id_column="cliente_id")
        usuario_repo = UsuarioRepository(self.repo.db)
        await usuario_repo.update(cliente.usuario_id, {"activo": nuevo_estado}, id_column="usuario_id")
        return cliente_actualizado

    
    #funcion para listar los clientes con paginacion o por id
    async def list_clientes(self, cliente_id: Optional[int] = None, activo: Optional[bool] = None, skip: int = 0, limit: int = 100):
        # Vemos si se envio un id de cliente
        if cliente_id is not None:
            # Vemos si el cliente existe
            cliente = await self.repo.get_by_id(cliente_id, id_column="cliente_id")
            # Si no existe, mandamos un not found
            if not cliente:
                raise NotFoundException(detail="Id de Cliente no encontrado", error_code="ID_NOT_FOUND")
            # si existe pero se filtro por activo, verificamos que el estado del cliente sea igual al filtro
            if activo is not None and cliente.activo != activo:
                return 0, []
            #si no es asi, retornamos el cliente encontrado
            return 1, [cliente]
        # Si no se envio un id de cliente, verificamos si se filtro por activo
        if activo is not None:
            total = await self.repo.count(activo=activo)
            clientes = await self.repo.get_all(skip=skip, limit=limit, activo=activo)
            return total, clientes
        # Si no se filtro por activo, retornamos todos los clientes con paginacion
        else:
            total = await self.repo.count()
            clientes = await self.repo.get_all(skip=skip, limit=limit)
            return total, clientes
        
    async def get_cliente_id_autenticado(self, current_user: UsuarioModel) -> int:
        """Obtiene el ID del cliente asociado al usuario autenticado."""
        cliente = await self.repo.get_by_usuario_id(current_user.usuario_id)
        if not cliente:
            raise NotFoundException(detail="Cliente no encontrado para este usuario", error_code="CLIENTE_NOT_FOUND")
        return cliente.cliente_id