from flask import Flask, request
from api.controllers.auth_controller import auth_bp
from api.controllers.data_controller import data_bp
from api.controllers.prediction_controller import prediction_bp
from api.services.auth_service import token_required
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# Dosya yolu
prediction_file_path = os.getenv('PREDICTION_FILE')

# prediction.json dosyasını kontrol et ve var ise sil
if os.path.isfile(prediction_file_path):
    os.remove(prediction_file_path)

# Blueprint'leri uygulamaya ekleyin
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(data_bp, url_prefix='/data')
app.register_blueprint(prediction_bp, url_prefix='/predict')

# Token doğrulamasını belirli endpoint'lerde uygulayın
@app.before_request
def before_request():
    # Belirli endpoint'ler için token doğrulamasını kontrol edin
    if request.endpoint in ['data_bp.set_data', 'prediction_bp.predict']:
        token_required(lambda: None)()  # Token kontrolünü çağırın

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
