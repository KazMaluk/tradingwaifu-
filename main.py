from fastapi import FastAPI
import requests
import os

app = FastAPI()

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"

@app.post("/chat")
async def chat(request: dict):
    user_message = request.get("message", "").lower()
    personality = request.get("personality", "tsundere_trader")
    strategy = request.get("strategy", "long_term_holding")
    
    market_data = requests.get(COINGECKO_API_URL).json()
    btc_price = market_data["bitcoin"]["usd"]
    eth_price = market_data["ethereum"]["usd"]

    return {"response": f"BTC is at ${btc_price}, ETH is at ${eth_price}. {personality} mode activated for {strategy} strategy!"}
