from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

ORDERS_FILE = "orders.json"

# Inizializza il file se non esiste
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w") as f:
        json.dump({"orders": []}, f)


def load_orders():
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)


def save_orders(data):
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/send_order", methods=["POST"])
def send_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dati JSON mancanti"}), 400

    orders = load_orders()
    orders["orders"].append(data)
    save_orders(orders)
    return jsonify({"status": "ordine ricevuto"}), 200


@app.route("/get_orders", methods=["GET"])
def get_orders():
    orders = load_orders()
    return jsonify(orders), 200


@app.route("/delete_order", methods=["POST"])
def delete_order():
    data = request.get_json()
    if not data or "ticket" not in data:
        return jsonify({"error": "Ticket mancante"}), 400

    ticket = data["ticket"]
    orders = load_orders()
    orders["orders"] = [o for o in orders["orders"] if o.get("ticket") != ticket]
    save_orders(orders)
    return jsonify({"status": f"ordine {ticket} eliminato"}), 200


@app.route("/", methods=["GET"])
def index():
    return "Hedge API attiva", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
