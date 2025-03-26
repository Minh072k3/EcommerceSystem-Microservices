from flask import Flask, request, jsonify
import requests
import os
from routes.user_routes import user_bp
# from routes.customer_routes import customer_bp
# from routes.other_routes import (
#     cart_bp, order_bp, shipping_bp, 
#     payment_bp, product_bp
# )

app = Flask(__name__)

# Đăng ký các blueprint
app.register_blueprint(user_bp, url_prefix='/api/users')
# app.register_blueprint(customer_bp, url_prefix='/api/customers')
# app.register_blueprint(cart_bp, url_prefix='/api/carts')
# app.register_blueprint(order_bp, url_prefix='/api/orders')
# app.register_blueprint(shipping_bp, url_prefix='/api/shipping')
# app.register_blueprint(payment_bp, url_prefix='/api/payments')
# app.register_blueprint(product_bp, url_prefix='/api/products')

# Cấu hình CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "api_gateway"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)