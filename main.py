from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
ORDERS_FILE = 'orders.json'

def save_order(data):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(data, f)

def load_order():
    if not os.path.exists(ORDERS_FILE):
        return {}
    with open(ORDERS_FILE, 'r') as f:
        return json.load(f)

@app.route('/master/send_order', methods=['POST'])
def send_order():
    data = request.get_json()
    save_order(data)
    return jsonify({'status': 'ok'})

@app.route('/slave/fetch_order', methods=['GET'])
def fetch_order():
    return jsonify(load_order())

# 🔁 NON usare `app.run()` qui
