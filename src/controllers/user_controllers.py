# controllers/user_controllers.py
from flask import Blueprint, jsonify

user_bp = Blueprint('users', __name__)

@user_bp.route("/users")
def users():
    return jsonify({
        "message": "Users route"
    })

@user_bp.route("/users/<int:id>")
def get_user(id):
    return jsonify({
        "id": id,
        "name": "Sample User"
    })