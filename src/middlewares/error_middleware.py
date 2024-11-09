# src/middleware/error_middleware.py
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import traceback
import sys

class ErrorHandler:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        @app.errorhandler(Exception)
        def handle_exception(error):
            """Handle all exceptions"""
            
            # Get the error details
            error_type = type(error).__name__
            status_code = 500
            message = str(error)
            stack = None
            
            # If in development, include stack trace
            if app.debug:
                stack = traceback.format_exc()
            
            # Handle HTTPException (like 404, 405, etc.)
            if isinstance(error, HTTPException):
                status_code = error.code
                message = error.description
            
            # Handle SQLAlchemy errors
            elif isinstance(error, IntegrityError):
                status_code = 409
                message = "Database integrity error"
                if 'unique constraint' in str(error.orig).lower():
                    message = "Record already exists"
                
            elif isinstance(error, SQLAlchemyError):
                status_code = 500
                message = "Database error occurred"
            
            # Prepare the error response
            error_response = {
                "success": False,
                "error": {
                    "type": error_type,
                    "message": message,
                    "status": status_code
                }
            }
            
            if stack and app.debug:
                error_response["error"]["stack"] = stack.split('\n')
            
            # Log the error
            current_app.logger.error(f"Error: {error_type} - {message}")
            if stack:
                current_app.logger.error(f"Stack: {stack}")
            
            return jsonify(error_response), status_code

        @app.errorhandler(404)
        def not_found_error(error):
            return jsonify({
                "success": False,
                "error": {
                    "type": "NotFoundError",
                    "message": "Resource not found",
                    "status": 404,
                    "path": error.description
                }
            }), 404

        @app.errorhandler(405)
        def method_not_allowed_error(error):
            return jsonify({
                "success": False,
                "error": {
                    "type": "MethodNotAllowedError",
                    "message": f"Method {error.valid_methods[0]} not allowed",
                    "status": 405,
                    "allowed_methods": error.valid_methods
                }
            }), 405

        @app.errorhandler(400)
        def bad_request_error(error):
            return jsonify({
                "success": False,
                "error": {
                    "type": "BadRequestError",
                    "message": str(error),
                    "status": 400
                }
            }), 400