from flask import Flask,jsonify
from flask_cors import CORS
from src.extensions import db, migrate
from src.config.config import get_config
from src.middlewares.error_middleware import ErrorHandler
import logging
import os
def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Load configuration
    app.config.from_object(get_config())
 
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize error handler
    ErrorHandler(app)
    
    # Register blueprints
    from src.routes import api
    app.register_blueprint(api, url_prefix="/api/v1")
    @app.route('/')
    def index():
      return jsonify({
            "message": "Welcome to the API",
           "version": "1.0",
           "mode":os.getenv('FLASK_ENV'),
  })
    return app