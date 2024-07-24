import requests
import jwt
from dotenv import load_dotenv
import os
from functools import wraps
from flask import request, jsonify

# .env dosyasını yükleyin
load_dotenv()

# .env dosyasından bilgileri alın
token_url = os.getenv("TOKEN_URI")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
secret_key = os.getenv("SECRET_KEY")
gateway_url = os.getenv("GATEWAY_URI")


def get_jwt_token():
    # Token almak için HTTP isteği gönderme
    payload = {
        "username": username,
        "password": password
    }
    url = gateway_url + token_url
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        token = response.text  # Token'ı doğrudan yanıt metninden al
        return token
    else:
        return None


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            # Eğer token yoksa, token'ı almak için get_jwt_token() fonksiyonunu kullanabilirsiniz
            token = get_jwt_token()
            if not token:
                return jsonify({'message': 'Token is missing and could not be retrieved!'}), 403

        try:
            # Token'ı decode etme ve secret key kontrolü yapma
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            request.user = decoded_token  # İsteğe kullanıcı bilgilerini ekle
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated_function
