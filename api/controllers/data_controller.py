from flask import Blueprint, request, jsonify
from api.services.auth_service import token_required
from api.services.data_service import fetch_data
from model.preprocessing import preprocess
from model.sarimax_model import train_and_predict
from model.predict import predict_future
from datetime import datetime

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/SetData', methods=['POST'])
@token_required
def set_data():
    try:
        data = fetch_data()
        preprocessed_data = preprocess(data)
        models, avg_mse, avg_r2 = train_and_predict(preprocessed_data)
        current_date = datetime.now()
        predictions_df = predict_future(models, preprocessed_data, current_date)

        return jsonify({
            'avg_mse': avg_mse,
            'avg_r2': avg_r2,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
