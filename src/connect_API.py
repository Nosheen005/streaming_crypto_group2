import json
import requests
from requests import Session, Timeout, TooManyRedirects
from constants import COINMARKET_API
 
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
 
def get_crypto_data(symbols=["ADA", "CAKE"]):

    parameters = {
        "symbol": ",".join(symbols),
        "convert": "USD",
    }
 
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }
 
    session = Session()
    session.headers.update(headers)
 
    try:
        response = session.get(API_URL, params=parameters)
        data = json.loads(response.text).get("data")
        return {symbol: data.get(symbol) for symbol in symbols}
 
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None
 
if __name__ == "__main__":
    crypto_data = get_crypto_data(["ADA", "CAKE"])
    if crypto_data:
        print(json.dumps(crypto_data, indent=4))