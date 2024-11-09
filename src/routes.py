from flask import Blueprint
from .controllers.user_controllers import users
from .controllers.product_controllers import products

api = Blueprint('api', __name__)

api.register_blueprint(users, url_prefix="/users")
api.register_blueprint(products, url_prefix="/products")
