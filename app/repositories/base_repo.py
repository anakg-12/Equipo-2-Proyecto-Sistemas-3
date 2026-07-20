from typing import Generic, TypeVar, Type, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import func
from app.core.errores import NotFoundException

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    # Repositorio con operaciones CRUD genericas

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, **kwargs) -> ModelType:
        """Crea un nuevo registro"""
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def get_by_id(self, id: int, id_column: str = "id") -> Optional[ModelType]:
        """Obtiene un registro por su ID"""
        stmt = select(self.model).where(getattr(self.model, id_column) == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    async def get_by_id_or_fail(self, id: int, id_column: str = "id", entity_name: str = "Entidad") -> ModelType:
        """
        Obtiene un registro por su ID. 
        Si no existe, lanza automáticamente NotFoundException.
        """
        entity = await self.get_by_id(id, id_column)
        if not entity:
            raise NotFoundException(
                detail=f"Id de {entity_name} no encontrado", 
                error_code="ID_NOT_FOUND"
            )
        return entity

    async def get_all(self, skip: int = 0, limit: int = 100, **filters):
        stmt = select(self.model).offset(skip).limit(limit)
        if filters:
            stmt = stmt.filter_by(**filters)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(
        self, id: int, data: Dict[str, Any], id_column: str = "id"
    ) -> Optional[ModelType]:
        """Actualiza un registro existente"""
        stmt = (
            update(self.model)
            .where(getattr(self.model, id_column) == id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, id: int, id_column: str = "id") -> bool:
        """Elimina un registro físicamente (Retorna True si se elimino)"""
        stmt = delete(self.model).where(getattr(self.model, id_column) == id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def delete_logical(self, id: int, id_column: str = "id") -> bool:
        """
        Borrado logico: marca la columna 'activo' como False
        Asume que el modelo tiene una columna 'activo' (booleana)
        """
        if not hasattr(self.model, "activo"):
            raise AttributeError(
                f"El modelo {self.model.__name__} no tiene columna 'activo'"
            )
        stmt = (
            update(self.model)
            .where(getattr(self.model, id_column) == id)
            .values(activo=False)
            .returning(self.model)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def count(self, **filters) -> int:
        stmt = select(func.count()).select_from(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)

        result = await self.db.execute(stmt)
        return result.scalar() or 0
