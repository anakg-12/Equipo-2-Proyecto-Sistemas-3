from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from fastapi import Query
from decimal import Decimal

#Hacemos la clase de una evaluación biométrica inicial con todos los atributos necesarios
class EvaluacionBiometricaInicial(BaseModel):
    entrenador_id: int = Field(..., ge=1, description="ID del entrenador que realiza la evaluación")
    fecha: Optional[date] = Field(None, description="Fecha de la evaluación biométrica")
    peso: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2, gt=30,  description="Peso del cliente", example=75.5)
    estatura: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2, gt=0.5, description="Estatura del cliente", example=1.75)
    porcentaje_grasa: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2, gt=5 ,description="Porcentaje de grasa corporal del cliente", example=23.5)
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales sobre la evaluación")

#creamos una clase para la creación de una evaluación biométrica, que hereda de la clase inicial
class EvaluacionBiometricaCrear(EvaluacionBiometricaInicial):
    pass

#creamos una clase para la salida de una evaluación biométrica, que hereda de la clase inicial y agrega el campo de ID
class EvaluacionBiometricaSalida(EvaluacionBiometricaInicial):
    cliente_id: int = Field(..., description="ID del cliente asociado a la evaluación biométrica")
    evaluacion_id: int = Field(..., description="ID de la evaluación biométrica")
    model_config = ConfigDict(from_attributes=True)

#creamos una clase para los filtros de evaluación biométrica, con un filtro por ID del cliente y paginación
class EvaluacionBiometricaFiltros:
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="Filtrar por el ID del cliente"),
        page: int = Query(1, ge=1, description="Número de página"),
        limit: int = Query(20, ge=1, le=100, description="Evaluaciones por página")
    ):
        self.cliente_id = cliente_id
        self.page = page
        self.limit = limit  
