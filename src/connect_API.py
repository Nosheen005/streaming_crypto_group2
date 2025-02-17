from requests import Session
import json
from pprint import pprint
from constants import COINMARKET_API

def get_latest_coin_data(symbol="ADA"):
    API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    
    symbol = "ADA"
    

    parameters = {
        "symbol": symbol,
        "convert": "USD",
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }

    session = Session()
    session.headers.update(headers)
    
    response = session.get(API_URL, params=parameters)
    print(response.text)
    #return json.loads(response.text)["data"][symbol]

get_latest_coin_data()

