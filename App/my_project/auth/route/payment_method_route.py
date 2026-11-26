from flask import Blueprint, jsonify, request
from my_project.auth.controller.payment_method_controller import PaymentMethodController

payment_method_bp = Blueprint('payment_method_bp', __name__, url_prefix='/api/payment-methods')
controller = PaymentMethodController()

@payment_method_bp.route('', methods=['GET'])
def get_all_payment_methods():
    return jsonify(controller.find_all()), 200

@payment_method_bp.route('/<int:method_id>', methods=['GET'])
def get_payment_method_by_id(method_id: int):
    method = controller.find_by_id(method_id)
    if method:
        return jsonify(method), 200
    return jsonify({'error': 'Payment method not found'}), 404

@payment_method_bp.route('', methods=['POST'])
def create_payment_method():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@payment_method_bp.route('/<int:method_id>', methods=['PUT'])
def update_payment_method(method_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(method_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Payment method not found'}), 404

@payment_method_bp.route('/<int:method_id>', methods=['DELETE'])
def delete_payment_method(method_id: int):
    success = controller.delete(method_id)
    if success:
        return jsonify({'message': 'Payment method deleted successfully'}), 200
    return jsonify({'error': 'Payment method not found'}), 404

@payment_method_bp.route('/<int:method_id>/payments', methods=['GET'])
def get_payments_by_method(method_id: int):
    payments = controller.find_payments_by_method_id(method_id)
    if payments is not None:
        return jsonify(payments), 200
    return jsonify({'error': 'Payment method not found'}), 404
