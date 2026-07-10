from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from datetime import datetime, timezone
from http import HTTPStatus
from app.schemas.response import ErrorResponse 

from app.core.errores import AppException

def setup_exception_handlers(app: FastAPI):
    
    # 1. Errores de nuestras reglas de negocio (ej. "Membresía vencida")
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        try:
            error_phrase = HTTPStatus(exc.status_code).phrase
        except ValueError:
            error_phrase = "Error"
            
        error_response = ErrorResponse(
            error=error_phrase,
            codigoInterno=exc.error_code,
            mensaje=exc.detail,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        return JSONResponse(status_code=exc.status_code, content=error_response.model_dump(exclude_none=True))

    # 2. Errores de Validación (ej. el usuario mandó un texto en vez de un número)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # FastAPI usa 422 por defecto, pero forzamos 400 para cumplir tu regla
        status_code = 400 
        
        # Extraemos el primer error para ponerlo en el mensaje principal
        primer_error = exc.errors()[0]
        campo_fallido = primer_error.get("loc", [""])[-1]
        mensaje_detalle = f"Error en el campo '{campo_fallido}': {primer_error.get('msg')}"

        error_response = ErrorResponse(
            error="Bad Request",
            codigoInterno="VALIDATION_ERROR",
            mensaje=mensaje_detalle,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        return JSONResponse(status_code=status_code, content=error_response.model_dump(exclude_none=True))

    # 3. Errores HTTP generales (ej. URL no entrontrada 404, método no permitido 405)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
      try:
            error_phrase = HTTPStatus(exc.status_code).phrase
      except ValueError:
            error_phrase = "Error"
            
      error_response = ErrorResponse(
            error=error_phrase,
            codigoInterno="HTTP_ERROR",
            mensaje=str(exc.detail),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
      return JSONResponse(status_code=exc.status_code, content=error_response.model_dump(exclude_none=True))

    # 4. Errores críticos de Base de Datos (ej. insertar un correo que ya existe)
    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
        msg = str(exc.orig).lower()
        detail = "Error de integridad en la base de datos."
        status_code = 400
        error_code = "DATABASE_ERROR"

          #SI Hay dublicados en PostgreSQL (como misma cédula) se trata como conflicto (409)
        if "unique constraint" in msg or "duplicate key" in msg:
            detail = "El registro ya existe o viola una regla de unicidad."
            status_code = 409
            error_code = "UNIQUE_CONSTRAINT_VIOLATION"
        elif "foreign key constraint" in msg or "violates foreign key" in msg:
            detail = "Estás intentando usar un ID que no existe."
            status_code = 404 #Not found
            error_code = "INVALID_FOREIGN_KEY"
        try:
            error_phrase = HTTPStatus(status_code).phrase
        except ValueError:
            error_phrase = "Error"

        error_response = ErrorResponse(
            error=error_phrase,
            codigoInterno=error_code,
            mensaje=detail,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        return JSONResponse(status_code=status_code, content=error_response.model_dump(exclude_none=True))