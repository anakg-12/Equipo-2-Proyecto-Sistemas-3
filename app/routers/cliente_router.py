from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, requiere_rol
from app.bd.database import get_db
from app.schemas.membresia_cliente_schema import membresiaClienteSalida
from app.schemas.reserva_inscripcion_schema import reservaInscripcionSalida, reservaInscripcionEntrada
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.membresia_cliente_service import MembresiaClienteService
from app.models.usuario_model import UsuarioModel

from app.schemas.cliente_schema import (
    clienteInicial,
    clienteSalida, 
    clienteActualizar, 
    ClienteFiltros
)
from app.services.cliente_service import ClienteService
from app.services.reserva_inscripcion_service import ReservaInscripcionService

router = APIRouter(prefix="/api/v1/clientes", tags=["Módulo de Clientes"])

def get_service(db: AsyncSession = Depends(get_db)) -> ClienteService:
    return ClienteService(db)

def get_service_membresia(db: AsyncSession = Depends(get_db)) -> MembresiaClienteService:
    return MembresiaClienteService(db)

def get_service_reserva(db: AsyncSession = Depends(get_db)) -> ReservaInscripcionService:
    return ReservaInscripcionService(db)

@router.get("/",
            response_model=PaginatedResponse[clienteSalida],
            dependencies=[Depends(requiere_rol("Administracion"))])


async def listar_clientes(
    filtros: ClienteFiltros = Depends(), 
    service: ClienteService = Depends(get_service)
):
    """
    Lista todos los clientes (activos o inactivos según el filtro).
    Soporta filtro opcional por ID. 
    Accesible solo para Administración.
    """
    skip = (filtros.page - 1) * filtros.limit
    
    # Pasamos los filtros al servicio
    total, res = await service.list_clientes(
        cliente_id=filtros.cliente_id,
        activo=filtros.activo,
        skip=skip,
        limit=filtros.limit
    )
    if total == 0:
        return {
            "status": "success",
            "message": "No se encontraron clientes",
            "data": res,
            "total": total,
            "page": filtros.page,
            "limit": filtros.limit
        }
    if total == 1:
        return {
            "status": "success",
            "message": "Cliente encontrado exitosamente",
            "data": res,
            "total": total,
            "page": filtros.page,
            "limit": filtros.limit
        }
    
    return {
        "status": "success",
        "message": "Lista de clientes obtenida exitosamente",
        "data": res,
        "total": total,
        "page": filtros.page,
        "limit": filtros.limit
    }
    
@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=StandardResponse[clienteSalida],
             dependencies=[Depends(requiere_rol("Administracion"))])
async def crear_cliente(
    schema: clienteInicial,
    service: ClienteService = Depends(get_service)
):
    """
    Crea un nuevo cliente asociado a un usuario existente con rol de cliente.
    Accesible solo para Administración.
    """
    res = await service.create_cliente(schema)
    
    return {
        "status": "success",
        "message": "Cliente creado exitosamente",
        "data": res
    }

@router.patch("/{id}/estado", 
              response_model=StandardResponse[clienteSalida],
              dependencies= [Depends(requiere_rol(["Administracion"]))])
async def actualizar_estado_cliente(
    id: int,
    schema: clienteActualizar,
    service: ClienteService = Depends(get_service)
):
    """
    Permite actualizar el estado de un cliente.
    Accesible solo para Administración.
    """
    # En lugar de usar un diccionario crudo, pasamos el schema validado
    res = await service.update_estado_cliente(id, schema)
    
    return {
        "status": "success",
        "message": "Estado del cliente actualizado correctamente",
        "data": res
    }
@router.get("/{id}/estado-membresia", response_model=StandardResponse[membresiaClienteSalida], dependencies=[Depends(requiere_rol(["Administracion", "Finanzas"]))])
async def obtener_membresia_cliente(id: int, service: MembresiaClienteService = Depends(get_service_membresia)):

    """
    Permite consultar el estado de la membresia de un cliente, busqueda por ID.
     Accesible solo para Administración o Finanzas.
    """

    res = await service.saber_estado_membresia(id)
    if res["estado"] == "Ninguna":
        return {
            "status": "success",
            "message": "Membresia del cliente no encontrada",
            "data": res
        }
    return {
        "status": "success",
        "message": "Membresia del cliente obtenida exitosamente",
        "data": res
    }

@router.post("/me/reservas", response_model=StandardResponse[reservaInscripcionSalida])
async def crear_reserva_inscripcion(
    schema: reservaInscripcionEntrada,
    current_user: UsuarioModel = Depends(get_current_user),
    service: ClienteService = Depends(get_service),
    service_reserva: ReservaInscripcionService = Depends(get_service_reserva)
):
    
    """
    Permite la creación de reservas en sesiones programadas.
    Accesible para clientes. 
    """

    cliente_id = await service.get_cliente_id_autenticado(current_user)
    res = await service_reserva.crear_reserva_inscripcion(cliente_id, schema)
    return {
        "status": "success",
        "message": "Reserva de inscripción creada exitosamente",
        "data": res
    }