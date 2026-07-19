"""Constantes compartidas de la aplicación.

Colocar aquí listas y valores que se repiten en distintos módulos, p. ej.
los estados permitidos para recursos como sesiones y tickets.
"""

# Categorías de máquinas (pueden usarse para valores iniciales o validación)
MACHINE_CATEGORIES = [
    "Musculación",
    "Cardiovascular",
    "Peso Libre",
]

# Estados para sesiones programadas (valores canónicos)
SESSION_PROGRAMADA = "programada"
SESSION_COMPLETADA = "completada"
SESSION_CANCELADA = "cancelada"
SESSION_STATES = [SESSION_PROGRAMADA, SESSION_COMPLETADA, SESSION_CANCELADA]

# Estados para tickets de mantenimiento
TICKET_ABIERTO = "abierto"
TICKET_EN_PROCESO = "en_proceso"
TICKET_CERRADO = "cerrado"
TICKET_STATES = [TICKET_ABIERTO, TICKET_EN_PROCESO, TICKET_CERRADO]

# Estados para membresía
MEMBERSHIP_ACTIVA = "activa"
MEMBERSHIP_INACTIVA = "inactiva"
MEMBERSHIP_POR_VENCER = "por_vencer"
MEMBERSHIP_VENCIDA = "vencida"
MEMBERSHIP_NONE = "ninguna"
MEMBERSHIP_STATES = [
    MEMBERSHIP_ACTIVA,
    MEMBERSHIP_INACTIVA,
    MEMBERSHIP_POR_VENCER,
    MEMBERSHIP_VENCIDA,
]

# Estados habituales para reservas/inscripciones (se usan en varios servicios)
RESERVATION_ACTIVA = "activa"
RESERVATION_CANCELADA = "cancelada"
RESERVATION_ASISTIO = "asistio"
RESERVATION_STATES = [RESERVATION_ACTIVA, RESERVATION_CANCELADA, RESERVATION_ASISTIO]

# Estado operativo de las máquinas
MACHINE_OPERATIVE_ACTIVA = "activa"
MACHINE_OPERATIVE_EN_MANTENIMIENTO = "en_mantenimiento"
MACHINE_OPERATIVE_FUERA_DE_SERVICIO = "fuera_de_servicio"
MACHINE_OPERATIVE_STATES = [
    MACHINE_OPERATIVE_ACTIVA,
    MACHINE_OPERATIVE_EN_MANTENIMIENTO,
    MACHINE_OPERATIVE_FUERA_DE_SERVICIO,
]

# Mensajes y códigos reutilizables (ejemplos)
DEFAULT_SUCCESS_STATUS = "success"

# Tiempo por defecto para paginación (si se quiere centralizar)
DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10
