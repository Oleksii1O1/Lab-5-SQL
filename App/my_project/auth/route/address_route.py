from flask import Blueprint, jsonify, request
from my_project.auth.controller.address_controller import AddressController

address_bp = Blueprint('address_bp', __name__, url_prefix='/api/addresses')
controller = AddressController()

@address_bp.route('', methods=['GET'])
def get_all_addresses():
    return jsonify(controller.find_all()), 200

@address_bp.route('/<int:address_id>', methods=['GET'])
def get_address_by_id(address_id: int):
    address = controller.find_by_id(address_id)
    if address:
        return jsonify(address), 200
    return jsonify({'error': 'Address not found'}), 404

@address_bp.route('', methods=['POST'])
def create_address():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@address_bp.route('/<int:address_id>', methods=['PUT'])
def update_address(address_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(address_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Address not found'}), 404

@address_bp.route('/<int:address_id>', methods=['DELETE'])
def delete_address(address_id: int):
    success = controller.delete(address_id)
    if success:
        return jsonify({'message': 'Address deleted successfully'}), 200
    return jsonify({'error': 'Address not found'}), 404

@address_bp.route('/<int:address_id>/orders', methods=['GET'])
def get_orders_by_address(address_id: int):
    orders = controller.find_orders_by_address_id(address_id)
    if orders is not None:
        return jsonify(orders), 200
    return jsonify({'error': 'Address not found'}), 404
