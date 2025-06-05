from flask import Flask, request, jsonify

app = Flask(__name__)

# Memoria temporanea (non persistente)
hedge_data = {}

@app.route("/")
def index():
    return jsonify({"status": "Hedge API attiva"})

# === Nuovo endpoint universale /hedge ===

# MASTER invia l'ordine
@app.route("/hedge", methods=["POST"])
def hedge_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    required_fields = ["symbol", "action", "lot", "magic", "ticket"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    hedge_data["last_order"] = data
    return jsonify({"status": "ok", "received": data})

# SLAVE richiede l'ordine
@app.route("/hedge", methods=["GET"])
def hedge_get():
    if "last_order" in hedge_data:
        return jsonify(hedge_data["last_order"])
    else:
        return jsonify({"status": "no_order"})

# === Debug/testing legacy ===

@app.route("/open", methods=["POST"])
def open_trade():
    return hedge_post()

@app.route("/get", methods=["GET"])
def get_last_order():
    return hedge_get()

@app.route("/clear", methods=["POST"])
def clear_order():
    hedge_data.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
