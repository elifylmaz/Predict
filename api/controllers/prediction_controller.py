from flask import Blueprint, request, jsonify
from api.services.prediction_service import get_predictions
from api.services.auth_service import token_required

prediction_bp = Blueprint('prediction_bp', __name__)

@prediction_bp.route('/predict', methods=['GET'])
@token_required
def predict():
    try:
        # JSON formatında gelen verileri al
        data = request.get_json()

        # 'product_id' değerini al ve integer olarak dönüştür
        product_id = int(data['product_id'])

        # Tahminleri almak için prediction_service'den fonksiyonu çağır
        predictions = get_predictions(product_id)

        # Tahmin sonuçlarını JSON formatında döndür
        return jsonify(predictions)

    except Exception as e:
        # Hata durumunda hata mesajını JSON formatında döndür
        return jsonify({'error': str(e)}), 500
