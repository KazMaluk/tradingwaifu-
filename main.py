from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()
    
    if not user_message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
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
        return jsonify({"error": f"Error processing request: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
