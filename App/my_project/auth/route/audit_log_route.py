from flask import Blueprint, jsonify
from my_project.auth.controller.audit_log_controller import AnimatorAuditLogController

audit_log_bp = Blueprint('audit_log_bp', __name__, url_prefix='/api/audit-logs')
controller = AnimatorAuditLogController()

@audit_log_bp.route('', methods=['GET'])
def get_all_logs():
    return jsonify(controller.find_all()), 200

@audit_log_bp.route('/<int:log_id>', methods=['GET'])
def get_log_by_id(log_id: int):
    log = controller.find_by_id(log_id)
    if log:
        return jsonify(log), 200
    return jsonify({'error': 'Audit log record not found'}), 404

@audit_log_bp.route('/animator/<int:animator_id>', methods=['GET'])
def get_logs_by_animator(animator_id: int):
    return jsonify(controller.find_by_animator_id(animator_id)), 200
