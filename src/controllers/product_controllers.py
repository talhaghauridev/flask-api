# controllers/product_controllers.py
from flask import Blueprint, jsonify

# Create blueprint instance
products = Blueprint('products', __name__,)

@products.route("/")
def products_fun():
    return jsonify({
        "name": "Product",
        "route": "Product route"
    })

# You can add more product routes here
@products.route("/<int:id>")
def get_product(id):
    return jsonify({
        "id": id,
        "name": "Sample Product",
        "route": f"Product route for id {id}"
    })