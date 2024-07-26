import json
import os
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
        # Verileri almak için fetch_data fonksiyonunu çağır
        data = fetch_data()

        # Verileri ön işleme tabi tut
        preprocessed_data = preprocess(data)

        # Model eğitimini başlat ve sonuçları al
        print("Model eğitimi başlıyor...")
        models, avg_mse, avg_r2 = train_and_predict(preprocessed_data)
        print("Model eğitimi tamamlandı.")

        # Geçerli tarihi al
        current_date = datetime.now()

        # Gelecekteki tahminleri yap
        predictions_df = predict_future(models, preprocessed_data, current_date)

        # prediction_df'yi JSON formatında döndür
        predictions_json = predictions_df.to_json(orient='records')

        # Sonuçları JSON formatında döndür
        return jsonify({
            'avg_mse': avg_mse,
            'avg_r2': avg_r2,
            'predictions': json.loads(predictions_json),
            'message': 'Predictions processed successfully.'
        })

    except Exception as e:
        # Hata durumunda hata mesajını JSON formatında döndür
        return jsonify({'error': str(e)}), 500