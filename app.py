from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import requests

from statcast_engine import build_statcast_payload
from utils import sign_payload
from config import STATCAST_WEBHOOK_URL

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "Diamond Alpha Statcast Worker Running"}

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/run-statcast", methods=["POST"])
def run_statcast():
    data = request.json or {}
    player_id = data.get("player_id")

    if not player_id:
        return jsonify({"error": "player_id required"}), 400

    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

    payload = build_statcast_payload(player_id, start_date, end_date)

    signature = sign_payload(payload)

    headers = {
        "Content-Type": "application/json",
        "X-STATCAST-SIGNATURE": signature
    }

    try:
        response = requests.post(
            STATCAST_WEBHOOK_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        return jsonify({
            "status": "sent",
            "response_code": response.status_code,
            "payload": payload
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
