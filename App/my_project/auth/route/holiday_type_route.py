from flask import Blueprint, jsonify, request
from my_project.auth.controller.holiday_type_controller import HolidayTypeController

holiday_type_bp = Blueprint('holiday_type_bp', __name__, url_prefix='/api/holiday-types')
controller = HolidayTypeController()

@holiday_type_bp.route('', methods=['GET'])
def get_all_holiday_types():
    return jsonify(controller.find_all()), 200

@holiday_type_bp.route('/<int:holiday_type_id>', methods=['GET'])
def get_holiday_type_by_id(holiday_type_id: int):
    holiday_type = controller.find_by_id(holiday_type_id)
    if holiday_type:
        return jsonify(holiday_type), 200
    return jsonify({'error': 'Holiday type not found'}), 404

@holiday_type_bp.route('', methods=['POST'])
def create_holiday_type():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@holiday_type_bp.route('/<int:holiday_type_id>', methods=['PUT'])
def update_holiday_type(holiday_type_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(holiday_type_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Holiday type not found'}), 404

@holiday_type_bp.route('/<int:holiday_type_id>', methods=['DELETE'])
def delete_holiday_type(holiday_type_id: int):
    success = controller.delete(holiday_type_id)
    if success:
        return jsonify({'message': 'Holiday type deleted successfully'}), 200
    return jsonify({'error': 'Holiday type not found'}), 404

@holiday_type_bp.route('/<int:holiday_type_id>/orders', methods=['GET'])
def get_orders_by_holiday_type(holiday_type_id: int):
    orders = controller.find_orders_by_holiday_type_id(holiday_type_id)
    if orders is not None:
        return jsonify(orders), 200
    return jsonify({'error': 'Holiday type not found'}), 404
