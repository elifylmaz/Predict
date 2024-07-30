from flask import Blueprint, request, jsonify
from api.services.prediction_service import get_predictions
from api.services.auth_service import token_required

prediction_bp = Blueprint('prediction_bp', __name__)

@prediction_bp.route('/predict', methods=['GET'])
@token_required
def predict():
    try:
        data = request.get_json()

        product_id = int(data['product_id'])

        predictions = get_predictions(product_id)

        return jsonify(predictions)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
