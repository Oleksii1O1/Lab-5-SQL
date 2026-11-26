from flask import Blueprint, jsonify, request
from my_project.auth.controller.payment_controller import PaymentController

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/api/payments')
controller = PaymentController()

@payment_bp.route('', methods=['GET'])
def get_all_payments():
    return jsonify(controller.find_all()), 200

@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id: int):
    payment = controller.find_by_id(payment_id)
    if payment:
        return jsonify(payment), 200
    return jsonify({'error': 'Payment not found'}), 404

@payment_bp.route('', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(payment_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Payment not found'}), 404

@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id: int):
    success = controller.delete(payment_id)
    if success:
        return jsonify({'message': 'Payment deleted successfully'}), 200
    return jsonify({'error': 'Payment not found'}), 404
