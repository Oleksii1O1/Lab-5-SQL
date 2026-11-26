from flask import Blueprint, jsonify, request
from my_project.auth.controller.client_controller import ClientController

client_bp = Blueprint('client_bp', __name__, url_prefix='/api/clients')
controller = ClientController()

@client_bp.route('', methods=['GET'])
def get_all_clients():
    return jsonify(controller.find_all()), 200

@client_bp.route('/<int:client_id>', methods=['GET'])
def get_client_by_id(client_id: int):
    client = controller.find_by_id(client_id)
    if client:
        return jsonify(client), 200
    return jsonify({'error': 'Client not found'}), 404

@client_bp.route('', methods=['POST'])
def create_client():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@client_bp.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(client_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Client not found'}), 404

@client_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id: int):
    success = controller.delete(client_id)
    if success:
        return jsonify({'message': 'Client deleted successfully'}), 200
    return jsonify({'error': 'Client not found'}), 404

@client_bp.route('/<int:client_id>/orders', methods=['GET'])
def get_orders_by_client(client_id: int):
    orders = controller.find_orders_by_client_id(client_id)
    if orders is not None:
        return jsonify(orders), 200
    return jsonify({'error': 'Client not found'}), 404
