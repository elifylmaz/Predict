from flask import Blueprint, request, jsonify
from api.services.auth_service import token_required
from api.services.data_service import fetch_data
from model.preprocessing import preprocess
from model.model import train_and_predict
from model.predict import predict_future
from datetime import datetime

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/SetData', methods=['POST'])
@token_required
def set_data():
    try:
        data = fetch_data()
        print("Veri başarıyla alındı.")

        preprocessed_data = preprocess(data)

        print("Model eğitimi başlıyor...")
        models, avg_mse, avg_r2 = train_and_predict(preprocessed_data)
        print("Model eğitimi tamamlandı.")

        current_date = datetime.now()

        predictions_df = predict_future(models, preprocessed_data, current_date)
        print("Tahminler tamamlandı.")

        predictions_df.to_json('predictions.json', orient='records', lines=True)
        print("Tahminler kaydedildi.")

        return jsonify({
            'avg_mse': avg_mse,
            'avg_r2': avg_r2,
            'message': 'Predictions processed successfully.'
        })

    except Exception as e:
        return jsonify({'Error': str(e)}), 500