import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from src.models import User, db
from src.models.user import UserRole
from functools import wraps

blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')

def add_cors_headers(response):
    """Add CORS headers to response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Handle CORS preflight requests
@blueprint.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'status': 'ok'})
        return add_cors_headers(response)

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
                response = jsonify({'error': 'Invalid token format'})
                return add_cors_headers(response), 401
        
        if not token:
            response = jsonify({'error': 'Token is missing'})
            return add_cors_headers(response), 401
        
        try:
            # Decode token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.get(id=data['user_id'])
            if not current_user:
                response = jsonify({'error': 'User not found'})
                return add_cors_headers(response), 401
        except jwt.ExpiredSignatureError:
            response = jsonify({'error': 'Token has expired'})
            return add_cors_headers(response), 401
        except jwt.InvalidTokenError:
            response = jsonify({'error': 'Invalid token'})
            return add_cors_headers(response), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def encode_jwt_token(payload):
    """Helper function to encode JWT token and ensure it's a string"""
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token

@blueprint.route('/register/', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        response = jsonify({'error': 'Email and password are required'})
        return add_cors_headers(response), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        response = jsonify({'error': 'User with this email already exists'})
        return add_cors_headers(response), 400
    
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
        
        response = jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        })
        return add_cors_headers(response), 201
        
    except Exception as e:
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 400

@blueprint.route('/login/', methods=['POST'])
def login():
    """Login user with email and password"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        response = jsonify({'error': 'Email and password are required'})
        return add_cors_headers(response), 400
    
    try:
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            response = jsonify({'error': 'Invalid email or password'})
            return add_cors_headers(response), 401
        
        # Generate JWT token
        token = encode_jwt_token({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        })
        
        response = jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        })
        return add_cors_headers(response), 200
        
    except Exception as e:
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 400

@blueprint.route('/logout/', methods=['POST'])
@token_required
def logout(current_user):
    """Logout user (client should remove token)"""
    response = jsonify({'message': 'Logout successful'})
    return add_cors_headers(response), 200

@blueprint.route('/me/', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current user information"""
    response = jsonify(current_user.to_dict())
    return add_cors_headers(response), 200

@blueprint.route('/refresh/', methods=['POST'])
@token_required
def refresh_token(current_user):
    """Refresh JWT token"""
    token = encode_jwt_token({
        'user_id': current_user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    })
    
    response = jsonify({
        'message': 'Token refreshed successfully',
        'token': token
    })
    return add_cors_headers(response), 200

@blueprint.route('/change-password/', methods=['POST'])
@token_required
def change_password(current_user):
    """Change user password"""
    data = request.get_json()
    
    if not data or not data.get('current_password') or not data.get('new_password'):
        response = jsonify({'error': 'Current password and new password are required'})
        return add_cors_headers(response), 400
    
    # Verify current password
    if not check_password_hash(current_user.password_hash, data['current_password']):
        response = jsonify({'error': 'Current password is incorrect'})
        return add_cors_headers(response), 401
    
    try:
        # Update password
        current_user.password_hash = generate_password_hash(data['new_password'])
        db.session.commit()
        
        response = jsonify({'message': 'Password changed successfully'})
        return add_cors_headers(response), 200
        
    except Exception as e:
        response = jsonify({'error': str(e)})
        return add_cors_headers(response), 400
