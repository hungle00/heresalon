from flask import Blueprint, jsonify, request
from src.models import Salon

blueprint = Blueprint('salons', __name__, url_prefix='/api')

@blueprint.route('/salons/', methods=['GET'])
def get_salons():
    """Get all salons"""
    salons = Salon.list()
    return jsonify([salon.to_dict() for salon in salons])

@blueprint.route('/salons/<int:salon_id>/', methods=['GET'])
def get_salon(salon_id):
    """Get salon by ID"""
    salon = Salon.get(id=salon_id)
    if not salon:
        return jsonify({'error': 'Salon not found'}), 404
    return jsonify(salon.to_dict())
