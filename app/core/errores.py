class AppException(Exception):
    """Es la base para las excepciones personalizadas."""
    def __init__(self, detail: str, error_code: str, status_code: int):
        self.detail = detail
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.detail)

class NotFoundException(AppException): 
    #el recurso no existe (404)
    def __init__(self, detail: str = "El recurso no fue encontrado", error_code: str = "NOT_FOUND"):
        super().__init__(detail=detail, error_code=error_code, status_code=404)

class BusinessRuleException(AppException):
    #violación de una regla de negocio (409)
    def __init__(self, detail: str, error_code: str = "BUSINESS_RULE_VIOLATION"):
        super().__init__(detail=detail, error_code=error_code, status_code=409)

class UnauthorizedException(AppException):
    #acceso no autorizado, falta de Token o token expirado (401)
    def __init__(self, detail: str = "No autorizado o token expirado", error_code: str = "UNAUTHORIZED"):
        super().__init__(detail=detail, error_code=error_code, status_code=401)