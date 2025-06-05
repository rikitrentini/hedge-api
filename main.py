from flask import Flask, request, jsonify

app = Flask(__name__)

# Memoria temporanea (per test su Render)
hedge_data = {}

@app.route("/")
def index():
    return jsonify({"status": "Hedge API attiva"})

@app.route("/open", methods=["POST"])
def open_trade():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    symbol = data.get("symbol")
    action = data.get("action")
    lot = data.get("lot")
    magic = data.get("magic")
    ticket = data.get("ticket")
    
    if not all([symbol, action, lot, magic, ticket]):
        return jsonify({"error": "Missing fields"}), 400
    
    hedge_data["last_order"] = data
    return jsonify({"status": "ok", "received": data})

@app.route("/get", methods=["GET"])
def get_last_order():
    if "last_order" in hedge_data:
        return jsonify(hedge_data["last_order"])
    else:
        return jsonify({"status": "no_order"})

@app.route("/clear", methods=["POST"])
def clear_order():
    hedge_data.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
