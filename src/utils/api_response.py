# src/utils/api_response.py
from flask import jsonify
from typing import Any

class ApiResponse:
    def __init__(
        self,
        status_code: int = 200,
        message: str = "Success",
        data: Any = None,
        **kwargs 
    ):
    
        # Base response structure
        self.response = {
            "status_code": status_code,
            "message": message,
            "suceess":True
        }

        # Add data if provided
        if data is not None:
            self.response["data"] = data
            
        # Add any additional fields
        self.response.update(kwargs)
    
    def send(self):
        """Send the formatted response"""
        return jsonify(self.response), self.response["status_code"]