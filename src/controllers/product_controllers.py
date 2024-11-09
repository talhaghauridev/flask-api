# controllers/product_controllers.py
from flask import Blueprint, jsonify

# Create blueprint instance
product_bp = Blueprint('products', __name__,)

@product_bp.route("/products")
def products():
    return jsonify({
        "name": "Product",
        "route": "Product route"
    })

# You can add more product routes here
@product_bp.route("/products/<int:id>")
def get_product(id):
    return jsonify({
        "id": id,
        "name": "Sample Product",
        "route": f"Product route for id {id}"
    })