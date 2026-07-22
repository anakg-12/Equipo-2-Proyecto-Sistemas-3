from enum import Enum


class RoleConstants:
    ADMIN = "Administración"
    TRAINER = "Entrenador"
    CLIENT = "Cliente"
    FINANCE = "Finanzas"


class MachineStatus(str, Enum):
    activa = "activa"
    en_mantenimiento = "en_mantenimiento"
    fuera_de_servicio = "fuera_de_servicio"


class SessionState(str, Enum):
    programada = "programada"
    completada = "completada"
    cancelada = "cancelada"


class TicketState(str, Enum):
    abierto = "abierto"
    en_proceso = "en_proceso"
    cerrado = "cerrado"


class ReservationState(str, Enum):
    activa = "activa"
    cancelada = "cancelada"
    asistio = "asistio"


class MembershipState(str, Enum):
    activa = "activa"
    inactiva = "inactiva"
    por_vencer = "por_vencer"
    vencida = "vencida"
    ninguna = "ninguna"


class SaleState(str, Enum):
    completada = "completada"
    cancelada = "cancelada"


class ProductCategory(str, Enum):
    accesorios = "Accesorios"
    suplementos = "Suplementos"


class PayMethod(str, Enum):
    efectivo = "Efectivo"
    transferencia = "Transferencia"
    pago_movil = "Pago móvil"


# Categorías de máquinas (human-friendly)
MACHINE_CATEGORIES = [
    "Musculación",
    "Cardiovascular",
    "Peso Libre",
]

# Listas derivadas (útiles para validaciones rápidas en routers)
SESSION_STATES = [s.value for s in SessionState]
TICKET_STATES = [s.value for s in TicketState]
RESERVATION_STATES = [s.value for s in ReservationState]
MEMBERSHIP_STATES = [s.value for s in MembershipState]
MACHINE_OPERATIVE_STATES = [s.value for s in MachineStatus]
SALE_STATES = [s.value for s in SaleState]

# Mensajes y códigos reutilizables (ejemplos)
DEFAULT_SUCCESS_STATUS = "success"

# Tiempo por defecto para paginación (si se quiere centralizar)
DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10
