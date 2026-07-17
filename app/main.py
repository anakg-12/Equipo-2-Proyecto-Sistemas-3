from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import setup_exception_handlers

from app.middlewares.logging_middleware import LoggingMiddleware

from app.bd.database import async_engine, Base

from app.routers import(
    cliente_router,
    control_acceso_router,
    entrenador_router,
    evaluacion_biometrica_router,
    maquina_router,
    membresia_cliente_router,
    plan_suscripcion_router,
    producto_tienda_router,
    reserva_inscripcion_router,
    sesion_programada_router,
    ticket_mantenimiento_router,
    usuario_router,
    venta_tienda_router,
    pago_factura_router
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creación de tablas de forma ASÍNCRONA 
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        yield # Aquí la API atiende peticiones
    
    # Al cerrar: Limpieza obligatoria
    await async_engine.dispose()    
    

app = FastAPI(title="SmartGym API", 
              version="1.0.0", 
              lifespan=lifespan
              )

# 1. Configuración de CORS (Para que el Frontend se pueda conectar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Registrar el Middleware de Logging
# Esto hará que cada petición se registre automáticamente
app.add_middleware(LoggingMiddleware)  

setup_exception_handlers(app)


app.include_router(cliente_router.router)
app.include_router(control_acceso_router.router)
app.include_router(entrenador_router.router)
app.include_router(evaluacion_biometrica_router.router)
app.include_router(maquina_router.router)
app.include_router(membresia_cliente_router.router)
app.include_router(pago_factura_router.router)
app.include_router(plan_suscripcion_router.router)
app.include_router(producto_tienda_router.router)
app.include_router(reserva_inscripcion_router.router)
app.include_router(sesion_programada_router.router)
app.include_router(ticket_mantenimiento_router.router)
app.include_router(usuario_router.router)
app.include_router(venta_tienda_router.router)