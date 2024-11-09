from flask import Flask, jsonify, Blueprint
from src.controllers import user_controllers, product_controllers
def create_app():
    app = Flask(__name__)
    
    # Import and register blueprints
  
    try :
      app.register_blueprint(product_controllers.product_bp, url_prefix='/api/v1')
      app.register_blueprint(user_controllers.user_bp, url_prefix='/api/v1')
    except Exception as e:
     print(e)
    
    # Add a default route
    @app.route('/')
    def index():
        return jsonify({
            "message": "Welcome to the API",
            "version": "1.0"
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)