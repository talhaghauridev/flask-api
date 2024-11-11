from flask import Blueprint, request
from src.models.user_model import User
from src.extensions import db
from src.utils.exceptions import AppError
from src.utils.api_response import ApiResponse
import re

users = Blueprint('users', __name__)

@users.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data:
        raise AppError.validation_error("No data provided")
    username = data.get('username')
    email = data.get('email')
    
    # Validate required fields
    if not username:
        raise AppError.validation_error("Username is required", {"field": "username"})
    if not email:
        raise AppError.validation_error("Email is required", {"field": "email"})
    
    # Validate email format
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        raise AppError.validation_error("Invalid email format", {"field": "email"})
    
    # Check existing user
    check_user = User.query.filter_by(email=email).first()
    if check_user:
        raise AppError(
            message="User already exists",
            status_code=409,
            error_type="DuplicateError",
            details={"field": "email"}
        )
    
    try:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        
        # Using created() for 201 status
        return ApiResponse.created(
            message="User created successfully",
            data=user.to_dict()
        )
        
    except Exception as e:
        db.session.rollback()
        raise AppError.database_error(f"Could not create user: {str(e)}")

@users.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        raise AppError.not_found(f"User with id {id} not found")
    
    # Using success() for 200 status
    return ApiResponse.success(
        message="User fetched successfully",
        data=user.to_dict()
    )

@users.route('/', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        # Using send() directly
        return ApiResponse.send(
            message="Users fetched successfully",
            data=[user.to_dict() for user in users]
        )
    except Exception as e:
        raise AppError.database_error(f"Error fetching users: {str(e)}")