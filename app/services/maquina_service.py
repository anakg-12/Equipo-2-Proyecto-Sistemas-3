from typing import Optional

from app.repositories import MaquinaRepository
from app.repositories.categoria_repo import CategoriaRepository
from app.schemas.maquina_schema import maquinaCrear, maquinaActualizar
from app.models import MaquinaModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errores import NotFoundException

class maquinaService:
    def __init__(self, db: AsyncSession):
        self.maquina_repo = MaquinaRepository(db)
        self.categoria_repo = CategoriaRepository(db)

    #crear maquina
    async def create_maquina(self, schema: maquinaCrear) -> MaquinaModel:
        #verificamos que la categoria exista
        categoria = await self.categoria_repo.get_by_id(schema.categoria_id, id_column="categoria_id")
        #si no hay categoria
        if not categoria:
            raise NotFoundException(detail="Categoría no encontrada", error_code="CATEGORIA_NOT_FOUND")
        maquina_info = schema.model_dump()
        return await self.maquina_repo.create(**maquina_info)

    #buscar la mquina por su ID
    async def get_maquina(self, id: int) -> MaquinaModel:
        maquina_buscada = await self.maquina_repo.get_by_id(id, id_column="maquina_id")
        if not maquina_buscada:
            raise NotFoundException(detail="Id de Máquina no encontrado", error_code="ID_NOT_FOUND")
        return maquina_buscada
    
    #actualizar el estado operativo de la maquina
    async def update_maquina_estado(self, id: int, schema: maquinaActualizar) -> MaquinaModel:
        maquina_buscada = await self.maquina_repo.get_by_id(id, id_column="maquina_id")
        if not maquina_buscada:
            raise NotFoundException(detail="Id de Máquina no encontrado", error_code="ID_NOT_FOUND")
        actualizar_info = schema.model_dump(exclude_unset=True)
        return await self.maquina_repo.update(id, actualizar_info, id_column="maquina_id")
    
    #listar maquinas con filtros por categoria y paginación
    async def list_maquinas(self, id: Optional[int] = None, categoria_nombre: str = None, skip: int = 0, limit: int = 100):
        if id is not None:
            maquina = await self.maquina_repo.get_by_id(id, id_column="maquina_id")
            if not maquina:
                raise NotFoundException(detail="Id de Máquina no encontrado", error_code="ID_NOT_FOUND")
            if categoria_nombre is not None:
                categoria = await self.categoria_repo.get_by_nombre(categoria_nombre.lower())
                if not categoria:
                    raise NotFoundException(detail="Categoría no encontrada", error_code="CATEGORIA_NOT_FOUND")
                if maquina.categoria_id != categoria.categoria_id:
                    return 0, []
            if skip > 0:
                return 1, []
            return 1, [maquina]
        if categoria_nombre is not None:
            categoria = await self.categoria_repo.get_by_nombre(categoria_nombre.lower())
            if not categoria:
                raise NotFoundException(detail="Categoría no encontrada", error_code="CATEGORIA_NOT_FOUND")
            total = await self.maquina_repo.count(categoria_id=categoria.categoria_id)
            maquinas = await self.maquina_repo.get_all(skip=skip, limit=limit, categoria_id=categoria.categoria_id)
            return total, maquinas
        else:
            total = await self.maquina_repo.count()
            maquinas = await self.maquina_repo.get_all(skip=skip, limit=limit)
            return total, maquinas
