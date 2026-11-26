from flask import Blueprint, jsonify, request
from my_project.auth.controller.role_controller import RoleController

role_bp = Blueprint('role_bp', __name__, url_prefix='/api/roles')
controller = RoleController()

@role_bp.route('', methods=['GET'])
def get_all_roles():
    return jsonify(controller.find_all()), 200

@role_bp.route('/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id: int):
    role = controller.find_by_id(role_id)
    if role:
        return jsonify(role), 200
    return jsonify({'error': 'Role not found'}), 404

@role_bp.route('', methods=['POST'])
def create_role():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    created = controller.create(data)
    return jsonify(created), 201

@role_bp.route('/<int:role_id>', methods=['PUT'])
def update_role(role_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    updated = controller.update(role_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Role not found'}), 404

@role_bp.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id: int):
    success = controller.delete(role_id)
    if success:
        return jsonify({'message': 'Role deleted successfully'}), 200
    return jsonify({'error': 'Role not found'}), 404
