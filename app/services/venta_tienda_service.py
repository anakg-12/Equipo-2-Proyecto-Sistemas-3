from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.venta_tienda_repo import VentaTiendaRepository
from app.repositories.venta_detalle_repo import VentaDetalleRepository
from app.services.producto_tienda_service import ProductoTiendaService
from app.schemas.venta_tienda_schema import VentaCompletaEntrada
from app.models import VentaTiendaModel
from app.core.errores import NotFoundException, BusinessRuleException
from app.constants import SaleState


class VentaTiendaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.venta_repo = VentaTiendaRepository(db)
        self.detalle_repo = VentaDetalleRepository(db)
        self.producto_service = ProductoTiendaService(db)

    async def registrar_venta(self, schema: VentaCompletaEntrada) -> VentaTiendaModel:
        # validacion estricta
        total_calculado = 0

        for item in schema.items:
            # Necesitamos consultar el producto real.
            producto = await self.producto_service.obtener_producto(item.producto_id)

            if not producto:
                raise NotFoundException(
                    detail=f"El producto con ID {item.producto_id} no existe",
                    error_code="PRODUCTO_NOT_FOUND",
                )

            # Verificamos si el precio enviado coincide con el de la base de datos
            if item.precio_unitario != producto.precio:
                raise BusinessRuleException(
                    detail=f"El precio enviado ({item.precio_unitario}) para '{producto.nombre}' es incorrecto. El precio real es {producto.precio}.",
                    error_code="PRECIO_INVALIDO",
                )

            # Sumamos el total usando el precio del backend, no el del cliente
            total_calculado += item.cantidad * producto.precio

            # Validar si el dinero alcanza
        if schema.monto_entregado < total_calculado:
            raise BusinessRuleException(
                detail=f"Fondos insuficientes. El total es {total_calculado} y se entregó {schema.monto_entregado}.",
                error_code="FONDOS_INSUFICIENTES",
            )

        # Calcular el vuelto
        vuelto = schema.monto_entregado - total_calculado

        # Descontar stock
        for item in schema.items:
            await self.producto_service.descontar_stock(item.producto_id, item.cantidad)

        # 4. Crear cabecera y detalles
        venta = await self.venta_repo.create(
            cliente_id=schema.cliente_id, total=total_calculado, estado=SaleState.completada.value
        )

        for item in schema.items:
            await self.detalle_repo.create(
                venta_id=venta.venta_id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=item.cantidad * item.precio_unitario,
            )

        await self.db.refresh(venta)

        # 5. Retornamos ambas cosas
        return venta, vuelto

    async def listar_ventas(
        self,
        cliente_id: int = None,
        fecha_desde=None,
        fecha_hasta=None,
        skip: int = 0,
        limit: int = 20,
    ):
        """Lista ventas con filtros opcionales y con paginacion"""
        return await self.venta_repo.get_all_with_filters(
            cliente_id, fecha_desde, fecha_hasta, skip, limit
        )

    async def obtener_venta_completa(self, venta_id: int):
        venta = await self.venta_repo.get_by_id_or_fail(
            venta_id, id_column="venta_id", entity_name="Venta"
        )
        detalles = await self.detalle_repo.get_by_venta(venta_id)
        return venta, detalles

    # Actualizar el estado de una venta :)
    async def actualizar_estado(self, venta_id: int, nuevo_estado: str):
        """Actualiza el estado de una venta. Si el nuevo estado es 'cancelada',
        se reponen las cantidades al stock de cada producto del detalle."""
        venta = await self.venta_repo.get_by_id(venta_id, id_column="venta_id")
        if not venta:
            raise NotFoundException(detail="Venta no encontrada", error_code="VENTA_NOT_FOUND")

        estado_anterior = getattr(venta, "estado", None)
        # Si ya está en el mismo estado, no hacemos nada
        if estado_anterior == nuevo_estado:
            return venta

        # Si transiciona a cancelada, sumar stock por cada detalle
        if nuevo_estado == SaleState.cancelada.value:
            detalles = await self.detalle_repo.get_by_venta(venta_id)
            for d in detalles:
                # cada detalle tiene producto_id y cantidad
                await self.producto_service.sumar_stock(d.producto_id, d.cantidad)

        # Actualizamos el estado en la cabecera de la venta
        actualizado = await self.venta_repo.update(venta_id, {"estado": nuevo_estado}, id_column="venta_id")
        return actualizado
