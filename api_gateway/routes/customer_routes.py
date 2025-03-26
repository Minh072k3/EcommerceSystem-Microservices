from flask import Blueprint, request, jsonify
import requests
import os
from functools import wraps
from user_routes import token_required

customer_bp = Blueprint('customer_bp', __name__)

USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user_service:8000')
CUSTOMER_SERVICE_URL = os.environ.get('CUSTOMER_SERVICE_URL', 'http://customer_service:8006')

@customer_bp.route('/profiles/', methods=['GET'])
@token_required
def get_customer_profiles(current_user):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/profiles/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/profiles/<profile_id>/', methods=['GET'])
@token_required
def get_customer_profile(current_user, profile_id):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/profiles/{profile_id}/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/regular/', methods=['GET'])
@token_required
def get_regular_customers(current_user):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/regular/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/premium/', methods=['GET'])
@token_required
def get_premium_customers(current_user):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/premium/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/corporate/', methods=['GET'])
@token_required
def get_corporate_customers(current_user):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/corporate/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/guest/', methods=['POST'])
def create_guest_customer():
    data = request.json
    response = requests.post(
        f"{CUSTOMER_SERVICE_URL}/api/customers/guest/",
        json=data
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/rewards/', methods=['GET'])
@token_required
def get_reward_points(current_user):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/rewards/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/benefits/', methods=['GET'])
@token_required
def get_premium_benefits(current_user):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/benefits/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/invoices/', methods=['GET'])
@token_required
def get_invoices(current_user):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/invoices/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code

@customer_bp.route('/order-history/<customer_id>/', methods=['GET'])
@token_required
def get_order_history(current_user, customer_id):
    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/order-history/{customer_id}/",
        headers={"Authorization": request.headers.get('Authorization')}
    )
    return jsonify(response.json()), response.status_code