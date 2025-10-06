from flask import Blueprint, jsonify, request
from src.models import Service, SalonService, Salon
from src.models.service import ServiceType

blueprint = Blueprint('services', __name__, url_prefix='/api')

@blueprint.route('/salons/<int:salon_id>/services/', methods=['GET'])
def get_services(salon_id):
    """Get all services or services for a specific salon"""
    salon = Salon.get(id=salon_id)
    
    if salon_id:
        # Get services for a specific salon
        salon = Salon.query.get(salon_id)
        if not salon:
            return jsonify({'error': 'Salon not found'}), 404
        
        # Get services through salon_services relationship
        salon_services = SalonService.query.filter_by(salon_id=salon_id).all()
        services = [salon_service.service for salon_service in salon_services]
        
        return jsonify([service.to_dict() for service in services])
    else:
        return jsonify({'error': 'Salon not found'}), 404


@blueprint.route('/services/<int:service_id>/', methods=['GET'])
def get_service(service_id):
    """Get service by ID"""
    service = Service.get(id=service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify(service.to_dict())
