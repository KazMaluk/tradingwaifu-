from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from hypercorn.asyncio import serve
from hypercorn.config import Config

app = Flask(__name__, static_folder="static")

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

@app.route("/")
def serve_home():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").lower()

        if not user_message:
            return jsonify({"error": "Please enter a message."}), 400

        # Fetch real-time market data from CoinGecko
        response = requests.get(COINGECKO_API_URL, timeout=10)
        response.raise_for_status()
        market_data = response.json()

        btc_price = market_data.get('bitcoin', {}).get('usd', 'N/A')
        eth_price = market_data.get('ethereum', {}).get('usd', 'N/A')

        market_summary = f"BTC: ${btc_price}, ETH: ${eth_price}."

        return jsonify({"response": f"Market Data: {market_summary}"})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Failed to retrieve market data due to a timeout."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to retrieve market data: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:" + os.getenv("PORT", "5000")]
    import asyncio
    asyncio.run(serve(app, config))
