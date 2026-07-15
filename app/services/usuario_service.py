from app.repositories import UsuarioRepository, RolRepository
from app.schemas.usuario_schema import usuarioEntrada, usuarioActualizar
from app.models import UsuarioModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password
from typing import Optional
from app.core.exceptions import AppException
from app.core.errores import NotFoundException
from app.core.security import hash_password

# Creamos la clase de Servicio de usuario
class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)
        self.rol_repo = RolRepository(db)

    async def authenticate_user(self, username: str, password: str):
        user = await self.usuario_repo.get_by_username(username)  # buscar por username
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        # Verificamos que el usuario esté activo
        if not user.activo:
            raise AppException(detail="Usuario inactivo", error_code="USER_INACTIVE", status_code=403)
        return user
    #creamos la funcion de crear usuario
    async def create_usuario(self, schema: usuarioEntrada) -> UsuarioModel:
        #verificamos que el nickname exista
        existe_usuario = await self.usuario_repo.get_by_username(schema.username, id_column="username")
        if existe_usuario:
            raise AppException(detail="El usuario ya está registrado", error_code="USER_ALREADY_EXISTS", status_code=409)
        #verificamos que el correo exista
        existe_email = await self.usuario_repo.get_by_email(schema.email, id_column="email")
        if existe_email:
            raise AppException(detail="El correo electrónico ya está registrado", error_code="EMAIL_ALREADY_EXISTS", status_code=409)
        #verificamos que la cedula exista
        existe_cedula = await self.usuario_repo.get_by_cedula(schema.cedula, id_column="cedula")
        if existe_cedula:
            raise AppException(detail="La cédula ya está registrada", error_code="CEDULA_ALREADY_EXISTS", status_code=409)
        #Vemos si el rol existe
        rol = await self.rol_repo.get_by_id(schema.rol_id, id_column="rol_id")
        if not rol:
            raise NotFoundException(detail="Rol no encontrado", error_code="ROL_NOT_FOUND")
        password_hash = hash_password(schema.password_recibida)
        user_info = schema.model_dump()
        del user_info["password_recibida"]
        user_info["password_hash"] = password_hash

        if schema.rol_id == 4:  # rol Cliente
            user_info["activo"] = False  # El cliente se crea como inactivo por defecto
            # Ademas, actualizar el usuario a inactivo
        nuevo_usuario = await self.usuario_repo.create(**user_info)
        await self.db.commit()
        await self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    #Creamos la función para cambiar el estado del usuario
    async def update_estado_usuario(self, id: int, schema: usuarioActualizar) -> UsuarioModel:
        usuario_existente = await self.usuario_repo.get_by_id(id, id_column="usuario_id")
        if not usuario_existente:
            raise NotFoundException(detail="Id de Usuario no encontrado", error_code="ID_NOT_FOUND")
        actualizar_info = schema.model_dump(exclude_unset=True)
        return await self.usuario_repo.update(id, actualizar_info, id_column="usuario_id")
    
    #Creamos una funcion para obtener una lista de usuarios (20 usuarios)
    async def list_usuarios(self, usuario_id: Optional[int] = None, skip: int = 0, limit: int = 100):
        if usuario_id is not None:
            usuario = await self.usuario_repo.get_by_id(usuario_id, id_column="usuario_id")
            if not usuario:
                raise NotFoundException(detail="Id de Usuario no encontrado", error_code="ID_NOT_FOUND")
            if skip > 0:
                return 0, []
            return 1, [usuario]
        else:
            total = await self.usuario_repo.count()
            usuarios = await self.usuario_repo.get_all(skip=skip, limit=limit)
            return total, usuarios