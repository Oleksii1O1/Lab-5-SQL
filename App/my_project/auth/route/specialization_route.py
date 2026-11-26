from flask import Blueprint, jsonify, request
from my_project.auth.controller.specialization_controller import SpecializationController

specialization_bp = Blueprint('specialization_bp', __name__, url_prefix='/api/specializations')
controller = SpecializationController()

@specialization_bp.route('', methods=['GET'])
def get_all_specializations():
    return jsonify(controller.find_all()), 200

@specialization_bp.route('/<int:specialization_id>', methods=['GET'])
def get_specialization_by_id(specialization_id: int):
    specialization = controller.find_by_id(specialization_id)
    if specialization:
        return jsonify(specialization), 200
    return jsonify({'error': 'Specialization not found'}), 404

@specialization_bp.route('', methods=['POST'])
def create_specialization():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@specialization_bp.route('/<int:specialization_id>', methods=['PUT'])
def update_specialization(specialization_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(specialization_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Specialization not found'}), 404

@specialization_bp.route('/<int:specialization_id>', methods=['DELETE'])
def delete_specialization(specialization_id: int):
    success = controller.delete(specialization_id)
    if success:
        return jsonify({'message': 'Specialization deleted successfully'}), 200
    return jsonify({'error': 'Specialization not found'}), 404

@specialization_bp.route('/<int:specialization_id>/animators', methods=['GET'])
def get_animators_by_specialization(specialization_id: int):
    animators = controller.find_animators_by_specialization_id(specialization_id)
    if animators is not None:
        return jsonify(animators), 200
    return jsonify({'error': 'Specialization not found'}), 404
