from flask import Blueprint, jsonify, request
from my_project.auth.controller.animator_controller import AnimatorController

animator_bp = Blueprint('animator_bp', __name__, url_prefix='/api/animators')
controller = AnimatorController()

@animator_bp.route('', methods=['GET'])
def get_all_animators():
    return jsonify(controller.find_all()), 200

@animator_bp.route('/<int:animator_id>', methods=['GET'])
def get_animator_by_id(animator_id: int):
    animator = controller.find_by_id(animator_id)
    if animator:
        return jsonify(animator), 200
    return jsonify({'error': 'Animator not found'}), 404

@animator_bp.route('', methods=['POST'])
def create_animator():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@animator_bp.route('/<int:animator_id>', methods=['PUT'])
def update_animator(animator_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(animator_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Animator not found'}), 404

@animator_bp.route('/<int:animator_id>', methods=['DELETE'])
def delete_animator(animator_id: int):
    success = controller.delete(animator_id)
    if success:
        return jsonify({'message': 'Animator deleted successfully'}), 200
    return jsonify({'error': 'Animator not found'}), 404

@animator_bp.route('/<int:animator_id>/agencies', methods=['GET'])
def get_agencies_by_animator(animator_id: int):
    agencies = controller.find_agencies_by_animator_id(animator_id)
    if agencies is not None:
        return jsonify(agencies), 200
    return jsonify({'error': 'Animator not found'}), 404

@animator_bp.route('/<int:animator_id>/specializations', methods=['GET'])
def get_specializations_by_animator(animator_id: int):
    specs = controller.find_specializations_by_animator_id(animator_id)
    if specs is not None:
        return jsonify(specs), 200
    return jsonify({'error': 'Animator not found'}), 404
