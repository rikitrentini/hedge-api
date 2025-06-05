from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

ORDERS_FILE = 'orders.json'

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})

@app.route('/master/send_order', methods=['POST'])
def send_order():
    data = request.get_json()
    with open(ORDERS_FILE, 'w') as f:
        json.dump(data, f)
    return jsonify({'status': 'ok'})

@app.route('/slave/fetch_order', methods=['GET'])
def fetch_order():
    if not os.path.exists(ORDERS_FILE):
        return jsonify({})
    with open(ORDERS_FILE, 'r') as f:
        return jsonify(json.load(f))
