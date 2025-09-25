from flask import Blueprint, jsonify, request
from src.models import Service
from src.models.service import ServiceType

blueprint = Blueprint('services', __name__)

@blueprint.route('/services/', methods=['GET'])
def get_services():
    """Get all services"""
    services = Service.list()
    return jsonify([service.to_dict() for service in services])


@blueprint.route('/services/<int:service_id>/', methods=['GET'])
def get_service(service_id):
    """Get service by ID"""
    service = Service.get(id=service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify(service.to_dict())
