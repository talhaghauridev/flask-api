from flask import Blueprint
from src.controllers.user_controllers import users
from src.controllers.product_controllers import products

api = Blueprint('api', __name__)

api.register_blueprint(users, url_prefix="/users")
api.register_blueprint(products, url_prefix="/products")
