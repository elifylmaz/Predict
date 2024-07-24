from flask import Blueprint, jsonify
from api.services.auth_service import token_required, get_jwt_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    token = get_jwt_token()
    if token:
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Failed to obtain token'}), 401

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected():
    # Bu endpoint'e erişim token doğrulaması gerektirir
    return jsonify({'message': 'This is a protected endpoint!'})
