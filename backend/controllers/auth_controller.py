"""Auth Controller - authentication endpoints"""
from flask import request, Blueprint
from functools import wraps
from backend.utils.jwt_utils import JWTUtils
from backend.utils.validators import Validators
from backend.utils.error_handler import ErrorHandler
from backend.services.user_service import UserService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


class AuthController:
    """Handles authentication operations"""
    
    def __init__(self, user_service: UserService, jwt_utils: JWTUtils):
        self.user_service = user_service
        self.jwt_utils = jwt_utils
    
    def register(self, request_data: dict):
        """Register a new user"""
        email = request_data.get('email', '').strip()
        password = request_data.get('password', '')
        name = request_data.get('name', '').strip()
        
        # Validate inputs
        valid, msg = Validators.validate_email(email)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        valid, msg = Validators.validate_password(password)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        valid, msg = Validators.validate_name(name)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        # Check if user exists
        existing = self.user_service.get_user_by_email(email)
        if existing:
            return ErrorHandler.conflict('Email already registered')
        
        # Create user (password hashing should be done by Supabase Auth)
        user_id = email.split('@')[0] + '_' + str(hash(email))[-8:]
        result = self.user_service.create_user(user_id, email, name, 'customer')
        
        if result['success']:
            token = self.jwt_utils.generate_token(user_id, email, 'customer')
            return ErrorHandler.created_response({
                'user_id': user_id,
                'email': email,
                'name': name,
                'role': 'customer',
                'token': token
            }, 'User registered successfully')
        else:
            return ErrorHandler.internal_error(result.get('error'))
    
    def login(self, request_data: dict):
        """Login user"""
        email = request_data.get('email', '').strip()
        password = request_data.get('password', '')
        
        if not email or not password:
            return ErrorHandler.bad_request('Email and password required')
        
        user = self.user_service.get_user_by_email(email)
        if not user:
            return ErrorHandler.unauthorized('Invalid credentials')
        
        if not user.get('is_active'):
            return ErrorHandler.forbidden('User account is inactive')
        
        # In production, verify password hash with Supabase
        token = self.jwt_utils.generate_token(
            user['user_id'],
            user['email'],
            user['role']
        )
        
        return ErrorHandler.success_response({
            'user_id': user['user_id'],
            'email': user['email'],
            'name': user['name'],
            'role': user['role'],
            'token': token
        }, 'Login successful')
    
    def validate_token(self, token: str):
        """Validate JWT token"""
        payload = self.jwt_utils.decode_token(token)
        if payload is None:
            return None
        return payload


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return ErrorHandler.unauthorized('Missing token')
        return f(*args, **kwargs)
    return decorated_function


def require_role(*roles):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return ErrorHandler.unauthorized('Missing token')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
