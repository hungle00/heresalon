from flask import Blueprint, jsonify, request
from src.models import Service, Salon
from src.models.service import ServiceType

blueprint = Blueprint('services', __name__, url_prefix='/api')

@blueprint.route('/salons/<int:salon_id>/services/', methods=['GET'])
def get_services(salon_id):
    """Get all services for a specific salon"""
    salon = Salon.get(id=salon_id)
    if not salon:
        return jsonify({'error': 'Salon not found'}), 404
    
    # Get services directly using salon_id
    services = Service.query.filter_by(salon_id=salon_id).all()
    
    return jsonify([service.to_dict() for service in services])


@blueprint.route('/services/<int:service_id>/', methods=['GET'])
def get_service(service_id):
    """Get service by ID"""
    service = Service.get(id=service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify(service.to_dict())
