class APIError(Exception):
    """Base API Error"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

class ValidationError(APIError):
    """Validation Error"""
    def __init__(self, message):
        super().__init__(message, status_code=400)

class NotFoundError(APIError):
    """Not Found Error"""
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class AuthenticationError(APIError):
    """Authentication Error"""
    def __init__(self, message="Authentication required"):
        super().__init__(message, status_code=401)

class AuthorizationError(APIError):
    """Authorization Error"""
    def __init__(self, message="Not authorized"):
        super().__init__(message, status_code=403)