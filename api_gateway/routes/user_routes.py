from flask import Blueprint, request, jsonify
import requests
import os
from functools import wraps
import jwt

user_bp = Blueprint('user_bp', __name__)

USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user_service:8000')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Gửi token đến user_service để xác thực
            auth_response = requests.post(
                f"{USER_SERVICE_URL}/api/users/verify-token/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if auth_response.status_code != 200:
                return jsonify({'message': 'Token is invalid!'}), 401
            
            current_user = auth_response.json()
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    return decorated

@user_bp.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):
    response = requests.get(
        f"{USER_SERVICE_URL}/api/users/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    response = requests.post(
        f"{USER_SERVICE_URL}/api/users/",
        json=data
    )
    return jsonify(response.json()), response.status_code

@user_bp.route('/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    response = requests.get(
        f"{USER_SERVICE_URL}/api/users/{user_id}/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@user_bp.route('/<user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    data = request.json
    response = requests.put(
        f"{USER_SERVICE_URL}/api/users/{user_id}/",
        json=data,
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@user_bp.route('/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    response = requests.delete(
        f"{USER_SERVICE_URL}/api/users/{user_id}/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response = requests.post(
        f"{USER_SERVICE_URL}/api/users/login/",
        json=data
    )
    return jsonify(response.json()), response.status_code

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    response = requests.post(
        f"{USER_SERVICE_URL}/api/users/register/",
        json=data
    )
    return jsonify(response.json()), response.status_code