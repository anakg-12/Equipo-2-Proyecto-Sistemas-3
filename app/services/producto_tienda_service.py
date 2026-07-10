from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.producto_tienda_repo import ProductoTiendaRepository
from app.schemas.producto_tienda_schema import ProductoTiendaInicial, ProductoTiendaActualizar
from app.models import ProductoTiendaModel
from app.core.exceptions import AppException
from app.core.errores import NotFoundException

class ProductoTiendaService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductoTiendaRepository(db)

    async def crear_producto(self, schema: ProductoTiendaInicial) -> ProductoTiendaModel:
        #vemos si el precio es negativo o el stock es negativo, si es asi lanzamos error
        if schema.precio <= 0:
            raise AppException(detail="El precio debe ser mayor a 0", error_code="PRECIO_INVALIDO", status_code=400)
        if schema.stock <= 0:
            raise AppException(detail="El stock debe ser mayor a 0", error_code="STOCK_INVALIDO", status_code=400)
        return await self.repo.create(**schema.model_dump())

    async def listar_productos(
        self, categoria: str = None, stock_min: int = None, page: int = 1, limit: int = 20
    ):
        """Devuelve (total, lista) con filtros opcionales y lo de paginacion"""
        skip = (page - 1) * limit if page > 0 else 0
        return await self.repo.get_all_paginated(categoria, stock_min, skip, limit)

    async def actualizar_producto(
        self, producto_id: int, schema: ProductoTiendaActualizar
    ) -> ProductoTiendaModel:
        producto = await self.repo.get_by_id(producto_id, id_column="producto_id")
        if not producto:
            raise NotFoundException(detail="Producto no encontrado", error_code="PRODUCTO_NOT_FOUND")
        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(producto_id, update_data, id_column="producto_id")

    async def obtener_producto(self, producto_id: int) -> ProductoTiendaModel:
        producto = await self.repo.get_by_id(producto_id, id_column="producto_id")
        if not producto:
            raise NotFoundException(detail="Producto no encontrado", error_code="PRODUCTO_NOT_FOUND")
        return producto

    async def descontar_stock(self, producto_id: int, cantidad: int):
        """Descuenta stock de un producto. Lanza error si no hay suficiente stock o si el producto no existe"""
        producto = await self.obtener_producto(producto_id)
        if producto.stock < cantidad:
            raise AppException(
                detail=f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, requerido: {cantidad}",
                error_code="STOCK_INSUFICIENTE",
                status_code=409
            )
        if producto.stock == cantidad and (producto.stock - cantidad) == 0:
            raise AppException(
                detail=f"No se puede vender los productos '{producto.nombre}' ya que es te quedarias sin stock. Por favor, reabastezca antes de venderlo.",
                error_code="ULTIMO_PRODUCTO",
                status_code=409
            )
        nuevo_stock = producto.stock - cantidad
        await self.repo.update_stock(producto_id, nuevo_stock)