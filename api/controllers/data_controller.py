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
    # Token doğrulaması başarılıysa işlemleri yap
    try:
        # Fetch data
        data = fetch_data()

        # Process data and save as CSV
        preprocessed_data = preprocess(data)

        # Train the model and make predictions
        models, avg_mse, avg_r2 = train_and_predict(preprocessed_data)

        # Make predictions
        current_date = datetime.now()
        predictions_df = predict_future(models, preprocessed_data, current_date)

        # Return the results
        return jsonify({
            'avg_mse': avg_mse,
            'avg_r2': avg_r2,
            # 'predictions': predictions_df.to_json()  # Geriye dönecek veri formatına göre ayarlayın
        })

    except Exception as e:
        # Hata durumunda geri dönecek mesaj
        return jsonify({'error': str(e)}), 500
