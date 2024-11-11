from typing import Any, Optional, Dict

class AppError(Exception):
    """Single error class to handle all application errors"""
    def __init__(
        self, 
        message: str,
        status_code: int = 400,
        error_type: str = "Error",
        details: Optional[Dict] = None,
        code: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.details = details
        self.code = code

    def to_dict(self) -> Dict:
        """Convert error to dictionary format"""
        error_dict = {
            "success": False,
            "status_code": self.status_code,
            "error": {
                "type": self.error_type,
                "message": self.message
            }
        }
        
        if self.details:
            error_dict["error"]["details"] = self.details
            
        if self.code:
            error_dict["error"]["code"] = self.code
            
        return error_dict

    @classmethod
    def validation_error(cls, message: str, details: Optional[Dict] = None):
        return cls(message, status_code=400, error_type="ValidationError", details=details)

    @classmethod
    def not_found(cls, message: str = "Resource not found"):
        return cls(message, status_code=404, error_type="NotFoundError")

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized"):
        return cls(message, status_code=401, error_type="UnauthorizedError")

    @classmethod
    def forbidden(cls, message: str = "Forbidden"):
        return cls(message, status_code=403, error_type="ForbiddenError")

    @classmethod
    def database_error(cls, message: str = "Database error"):
        return cls(message, status_code=500, error_type="DatabaseError")