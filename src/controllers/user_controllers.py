from flask import Blueprint, jsonify, request
from src.models.user_model import User
from src.extensions import db
from src.utils.exceptions import ValidationError, NotFoundError,APIError
from src.utils.api_response import ApiResponse
import re

users = Blueprint('users', __name__)

@users.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data:
        raise ValidationError("No data provided")
    
    username = data.get('username')
    email = data.get('email')
    
    # Validate required fields
    if not username:
        raise ValidationError("Username is required")
    if not email:
        raise ValidationError("Email is required")
        
    # Validate email format
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        raise ValidationError("Invalid email format")
        
    # Create user
    checkUser = User.query.filter_by(email=email).first()
    if checkUser :
        raise APIError("User is already exist",500)
    try:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
     
      
        return ApiResponse(           
            data=user.to_dict()
      ).send()
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f"Could not create user: {str(e)}")

@users.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        raise NotFoundError(f"User with id {id} not found")
    
    return ApiResponse(
         data=user,
    ).send()
@users.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    
    return ApiResponse(
      data=[user.to_dict() for user in users],).send()
 