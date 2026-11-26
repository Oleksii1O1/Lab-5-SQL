from flask import Blueprint, jsonify, request
from my_project.auth.controller.order_controller import OrderController

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/orders')
controller = OrderController()

@order_bp.route('', methods=['GET'])
def get_all_orders():
    return jsonify(controller.find_all()), 200

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id: int):
    order = controller.find_by_id(order_id)
    if order:
        return jsonify(order), 200
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(order_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id: int):
    success = controller.delete(order_id)
    if success:
        return jsonify({'message': 'Order deleted successfully'}), 200
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/<int:order_id>/payments', methods=['GET'])
def get_payments_by_order(order_id: int):
    payments = controller.find_payments_by_order_id(order_id)
    if payments is not None:
        return jsonify(payments), 200
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/<int:order_id>/animators', methods=['GET'])
def get_animators_by_order(order_id: int):
    animators = controller.find_animators_by_order_id(order_id)
    if animators is not None:
        return jsonify(animators), 200
    return jsonify({'error': 'Order not found'}), 404
