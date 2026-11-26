from flask import Blueprint, jsonify, request
from my_project.auth.controller.order_status_controller import OrderStatusController

order_status_bp = Blueprint('order_status_bp', __name__, url_prefix='/api/order-statuses')
controller = OrderStatusController()

@order_status_bp.route('', methods=['GET'])
def get_all_order_statuses():
    return jsonify(controller.find_all()), 200

@order_status_bp.route('/<int:status_id>', methods=['GET'])
def get_order_status_by_id(status_id: int):
    status = controller.find_by_id(status_id)
    if status:
        return jsonify(status), 200
    return jsonify({'error': 'Order status not found'}), 404

@order_status_bp.route('', methods=['POST'])
def create_order_status():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@order_status_bp.route('/<int:status_id>', methods=['PUT'])
def update_order_status(status_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(status_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Order status not found'}), 404

@order_status_bp.route('/<int:status_id>', methods=['DELETE'])
def delete_order_status(status_id: int):
    success = controller.delete(status_id)
    if success:
        return jsonify({'message': 'Order status deleted successfully'}), 200
    return jsonify({'error': 'Order status not found'}), 404

@order_status_bp.route('/<int:status_id>/orders', methods=['GET'])
def get_orders_by_status(status_id: int):
    orders = controller.find_orders_by_status_id(status_id)
    if orders is not None:
        return jsonify(orders), 200
    return jsonify({'error': 'Order status not found'}), 404
