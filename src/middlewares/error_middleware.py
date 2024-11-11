from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.utils.exceptions import AppError
import traceback

class ErrorHandler:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        @app.errorhandler(AppError)
        def handle_app_error(error):
            return jsonify(error.to_dict()), error.status_code

        @app.errorhandler(Exception)
        def handle_exception(error):
            """Handle all exceptions"""
            
            # If it's our custom error, let the other handler deal with it
            if isinstance(error, AppError):
                raise error

            # Get the error details
            error_type = type(error).__name__
            status_code = 500
            message = str(error)
            
            # Handle different error types
            if isinstance(error, HTTPException):
                status_code = error.code
                message = error.description
            elif isinstance(error, IntegrityError):
                status_code = 409
                message = "Database integrity error"
                if 'unique constraint' in str(error.orig).lower():
                    message = "Record already exists"
            elif isinstance(error, SQLAlchemyError):
                status_code = 500
                message = "Database error occurred"

            # Log the error
            if app.debug:
                current_app.logger.error(f"Error: {error_type} - {message}")
                current_app.logger.error(f"Stack: {traceback.format_exc()}")

            # Create error response
            error_response = {
                "success": False,
                "status_code": status_code,
                "error": {
                    "type": error_type,
                    "message": message
                }
            }

            if app.debug:
                error_response["error"]["stack"] = traceback.format_exc().split('\n')

            return jsonify(error_response), status_code