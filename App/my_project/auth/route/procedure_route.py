from flask import Blueprint, jsonify, request
from my_project.auth.controller.procedure_controller import ProcedureController

procedure_bp = Blueprint('procedure_bp', __name__, url_prefix='/api/procedures')
controller = ProcedureController()

@procedure_bp.route('/insert-client', methods=['POST'])
def call_insert_client():
    data = request.get_json() or {}
    try:
        result = controller.insert_client(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@procedure_bp.route('/link-m2m', methods=['POST'])
def call_link_m2m():
    data = request.get_json() or {}
    try:
        result = controller.link_m2m(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@procedure_bp.route('/insert-nonames', methods=['POST'])
def call_insert_ten_nonames():
    try:
        result = controller.insert_ten_nonames()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@procedure_bp.route('/stats-avg', methods=['GET'])
def call_get_animators_above_avg():
    try:
        result = controller.get_animators_above_avg()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@procedure_bp.route('/cursor-split', methods=['POST'])
def call_cursor_split():
    try:
        result = controller.cursor_split()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
