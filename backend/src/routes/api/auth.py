import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import User, db
from src.models.user import UserRole
from functools import wraps

blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.get(id=data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def encode_jwt_token(payload):
    """Helper function to encode JWT token and ensure it's a string"""
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    # PyJWT 1.7.1 returns bytes, so we need to decode it
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token

@blueprint.route('/register/', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 400
    
    try:
        # Create new user
        user = User.create(
            username=data.get('username', data['email'].split('@')[0]),  # Use email prefix as username if not provided
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=UserRole.CUSTOMER  # Default role
        )
        
        # Generate JWT token
        token = encode_jwt_token({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        })
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/login/', methods=['POST'])
def login():
    """Login user with email and password"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    try:
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token = encode_jwt_token({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        })
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/logout/', methods=['POST'])
@token_required
def logout(current_user):
    """Logout user (client should remove token)"""
    return jsonify({'message': 'Logout successful'}), 200

@blueprint.route('/me/', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user information"""
    return jsonify({
        'user': current_user.to_dict()
    }), 200

@blueprint.route('/refresh/', methods=['POST'])
@token_required
def refresh_token(current_user):
    """Refresh JWT token"""
    try:
        # Generate new JWT token
        token = encode_jwt_token({
            'user_id': current_user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        })
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/change-password/', methods=['POST'])
@token_required
def change_password(current_user):
    """Change user password"""
    data = request.get_json()
    
    if not data or not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400
    
    try:
        # Verify current password
        if not check_password_hash(current_user.password_hash, data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Update password
        current_user.password_hash = generate_password_hash(data['new_password'])
        current_user.save()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
