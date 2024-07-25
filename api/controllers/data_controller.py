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

        # data.json dosyasının varlığını kontrol et
        if os.path.exists('data.json'):
            # Verileri ön işleme tabi tut
            preprocessed_data = preprocess(data)

            # SARIMAX modelini eğit ve tahmin yap
            models, avg_mse, avg_r2 = train_and_predict(preprocessed_data)

            # Geçerli tarihi al
            current_date = datetime.now()

            # Gelecekteki tahminleri yap
            predictions_df = predict_future(models, preprocessed_data, current_date)

            # Sonuçları JSON formatında döndür
            return jsonify({
                'avg_mse': avg_mse,
                'avg_r2': avg_r2,
            })
        else:
            return jsonify({'message': 'data.json dosyası bulunamadı, lütfen verileri kontrol edin.'}), 404

    except Exception as e:
        # Hata durumunda hata mesajını JSON formatında döndür
        return jsonify({'error': str(e)}), 500
