from flask import Blueprint, jsonify, request
from my_project.auth.controller.review_controller import ReviewController

review_bp = Blueprint('review_bp', __name__, url_prefix='/api/reviews')
controller = ReviewController()

@review_bp.route('', methods=['GET'])
def get_all_reviews():
    return jsonify(controller.find_all()), 200

@review_bp.route('/<int:review_id>', methods=['GET'])
def get_review_by_id(review_id: int):
    review = controller.find_by_id(review_id)
    if review:
        return jsonify(review), 200
    return jsonify({'error': 'Review not found'}), 404

@review_bp.route('', methods=['POST'])
def create_review():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        created = controller.create(data)
        return jsonify(created), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@review_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id: int):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    try:
        updated = controller.update(review_id, data)
        if updated:
            return jsonify(updated), 200
        return jsonify({'error': 'Review not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@review_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id: int):
    success = controller.delete(review_id)
    if success:
        return jsonify({'message': 'Review deleted successfully'}), 200
    return jsonify({'error': 'Review not found'}), 404

@review_bp.route('/animator/<int:animator_id>', methods=['GET'])
def get_reviews_by_animator(animator_id: int):
    return jsonify(controller.find_by_animator_id(animator_id)), 200
