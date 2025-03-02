from fastapi import FastAPI, HTTPException
import os
import requests
import sys
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    sys.stderr.write("[ERROR]: Missing OpenAI API key. Ensure it is set as an environment variable.\n")
    openai_api_available = False
else:
    openai_api_available = True

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"

app = FastAPI()

@app.post("/chat")
async def chat(message: dict):
    user_message = message.get("message", "").lower()
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Please enter a message.")
    
    try:
        # Fetch real-time BTC and ETH market data from CoinGecko
        response = requests.get(COINGECKO_API_URL, timeout=10)
        response.raise_for_status()
        market_data = response.json()
        
        btc_price = market_data.get('bitcoin', {}).get('usd', 'N/A')
        btc_change = market_data.get('bitcoin', {}).get('usd_24h_change', 'N/A')
        eth_price = market_data.get('ethereum', {}).get('usd', 'N/A')
        eth_change = market_data.get('ethereum', {}).get('usd_24h_change', 'N/A')
        
        if btc_price == 'N/A' or eth_price == 'N/A':
            raise HTTPException(status_code=500, detail="Error retrieving data from CoinGecko API.")
        
        market_summary = (
            f"BTC is currently at ${btc_price} with a 24-hour change of {btc_change:.2f}%. "
            f"ETH is at ${eth_price} with a 24-hour change of {eth_change:.2f}%"
        )
        
        # Call OpenAI GPT to analyze the market trend if API is available
        if openai_api_available:
            try:
                import openai
                openai.api_key = OPENAI_API_KEY
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a crypto trading assistant providing market trend analysis."},
                        {"role": "user", "content": f"Analyze BTC and ETH market trend based on this data: {market_summary}"}
                    ]
                )
                ai_response = response["choices"][0]["message"]["content"].strip()
            except Exception as e:
                sys.stderr.write(f"[ERROR]: OpenAI API Error: {e}\n")
                ai_response = "AI analysis is currently unavailable due to an issue with OpenAI's API. Please try again later."
        else:
            ai_response = "AI analysis is unavailable due to missing OpenAI API key."
        
        return {"response": ai_response}
    
    except requests.exceptions.Timeout:
        sys.stderr.write("[ERROR]: Request to CoinGecko API timed out.\n")
        raise HTTPException(status_code=504, detail="Failed to retrieve market data due to a timeout. Please try again later.")
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"[ERROR]: Error fetching market data: {e}\n")
        raise HTTPException(status_code=500, detail="Failed to retrieve market data. Please try again later.")
    except Exception as e:
        sys.stderr.write(f"[ERROR]: Error processing request: {e}\n")
        raise HTTPException(status_code=500, detail="Oops! There was an error processing your request.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
