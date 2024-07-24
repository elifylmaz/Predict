from flask import Flask
from api.controllers.auth_controller import auth_bp
from api.controllers.data_controller import data_bp
from api.controllers.prediction_controller import prediction_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(data_bp, url_prefix='/data')
app.register_blueprint(prediction_bp, url_prefix='/predict')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
