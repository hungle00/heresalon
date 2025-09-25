from flask import Blueprint, jsonify, request
from src.models import User
from src.models.user import UserRole

blueprint = Blueprint('users', __name__)  # No url_prefix

@blueprint.route('/users/', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.list()
    return jsonify([user.to_dict() for user in users])

@blueprint.route('/users/', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Username and email are required'}), 400
    
    try:
        user = User.create(
            username=data['username'],
            email=data['email'],
            password_hash=data.get('password_hash'),
            role=UserRole.CUSTOMER if data.get('role') != 'admin' else UserRole.ADMIN
        )
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/users/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = User.get(id=user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@blueprint.route('/users/<int:user_id>/', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    user = User.get(id=user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'role' in data:
            user.role = UserRole.ADMIN if data['role'] == 'admin' else UserRole.CUSTOMER
        
        user.save()
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/users/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    user = User.get(id=user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.delete()
    return jsonify({'message': 'User deleted successfully'})

