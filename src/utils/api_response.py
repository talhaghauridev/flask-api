# from flask import jsonify
# from typing import Any

# class ApiResponse:
#     def __init__(
#         self,
#         status_code: int = 200,
#         message: str = "Success",
#         data: Any = None,
#         **kwargs 
#     ):
    
#         # Base response structure
#         self.response = {
#             "status_code": status_code,
#             "message": message,
#             "suceess":True
#         }

#         # Add data if provided
#         if data is not None:
#             self.response["data"] = data
            
#         # Add any additional fields
#         self.response.update(kwargs)
    
#     def send(self):
#         """Send the formatted response"""
#         return jsonify(self.response), self.response["status_code"]


from flask import jsonify
from typing import Any, Dict, Optional, List

class ApiResponse:
    @staticmethod
    def send(
        message: str = "Success",
        data: Any = None,
        status_code: int = 200,
        **kwargs
    ):
        response = {
            "status_code": status_code,
            "message": message,
            "success": True
        }
        
        if data is not None:
            response["data"] = data
            
        response.update(kwargs)
        
        return jsonify(response), status_code

    @staticmethod
    def created(message: str = "Resource created successfully", data: Any = None, **kwargs):
        return ApiResponse.send(message, data, 201, **kwargs)

    @staticmethod
    def updated(message: str = "Resource updated successfully", data: Any = None, **kwargs):
        return ApiResponse.send(message, data, 200, **kwargs)

    @staticmethod
    def deleted(message: str = "Resource deleted successfully", **kwargs):
        return ApiResponse.send(message, None, 200, **kwargs)

    @staticmethod
    def list(
        items: List[Any],
        message: str = "Resources fetched successfully",
        page: Optional[int] = None,
        total: Optional[int] = None,
        **kwargs
    ):
        extra = {}
        if page is not None:
            extra["page"] = page
        if total is not None:
            extra["total"] = total
            
        return ApiResponse.send(message, items, 200, **extra, **kwargs)