import time
import logging
import os
import traceback
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# 1. Asegurar que exista la carpeta "logs"
# Si la carpeta no existe, Python la crea automáticamente para evitar que la app falle
if not os.path.exists('logs'):
    os.makedirs('logs')

# 2. Configurar el Logger de la aplicación
logger = logging.getLogger("SmartGymLogger")
logger.setLevel(logging.INFO)

# Evitar que los logs se impriman dobles cuando el servidor se recarga (con --reload)
if not logger.handlers:
    # Formato de cómo se verá cada línea de texto
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Manejador 1: Guarda en el archivo de texto
    file_handler = logging.FileHandler("logs/smartgym_api.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Manejador 2: Muestra en la consola/terminal en tiempo real
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Añadimos los manejadores a nuestro logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que intercepta todas las peticiones, mide el tiempo de respuesta,
    las guarda en un archivo de texto y captura los errores críticos (500).
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        method = request.method
        url = request.url.path

        try:
            # 3. La petición pasa al router y esperamos la respuesta del servidor
            response = await call_next(request)
            process_time = time.time() - start_time
            status_code = response.status_code

            mensaje_log = f"{method} {url} - Status: {status_code} - Tiempo: {process_time:.4f}s"

            # 4. Clasificamos el nivel del log según el código HTTP
            if status_code >= 400 and status_code < 500:
                # Errores del cliente (400, 401, 404) o Reglas de Negocio (409)
                logger.warning(mensaje_log)
            else:
                # Éxitos (200, 201)
                logger.info(mensaje_log)

            return response

        except Exception as e:
            # 5. Captura de Errores Fatales (Ej. error de sintaxis o caída de BD)
            process_time = time.time() - start_time
            
            logger.error(
                f"CRÍTICO: {method} {url} - Fallo interno del servidor - Tiempo: {process_time:.4f}s\n"
                f"Detalle del error: {str(e)}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            
            # Volvemos a lanzar la excepción para que el servidor responda apropiadamente
            raise e