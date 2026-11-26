from flask import Blueprint, jsonify, request
from my_project.auth.controller.agency_controller import AgencyController

agency_bp = Blueprint('agency_bp', __name__, url_prefix='/api/agencies')
controller = AgencyController()

@agency_bp.route('', methods=['GET'])
def get_all_agencies():
    return jsonify(controller.find_all()), 200

@agency_bp.route('/<int:agency_id>', methods=['GET'])
def get_agency_by_id(agency_id: int):
    agency = controller.find_by_id(agency_id)
    if agency:
        return jsonify(agency), 200
    return jsonify({'error': 'Agency not found'}), 404

@agency_bp.route('', methods=['POST'])
def create_agency():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@agency_bp.route('/<int:agency_id>', methods=['PUT'])
def update_agency(agency_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(agency_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Agency not found'}), 404

@agency_bp.route('/<int:agency_id>', methods=['DELETE'])
def delete_agency(agency_id: int):
    success = controller.delete(agency_id)
    if success:
        return jsonify({'message': 'Agency deleted successfully'}), 200
    return jsonify({'error': 'Agency not found'}), 404

@agency_bp.route('/<int:agency_id>/orders', methods=['GET'])
def get_orders_by_agency(agency_id: int):
    orders = controller.find_orders_by_agency_id(agency_id)
    if orders is not None:
        return jsonify(orders), 200
    return jsonify({'error': 'Agency not found'}), 404

@agency_bp.route('/<int:agency_id>/animators', methods=['GET'])
def get_animators_by_agency(agency_id: int):
    animators = controller.find_animators_by_agency_id(agency_id)
    if animators is not None:
        return jsonify(animators), 200
    return jsonify({'error': 'Agency not found'}), 404
