from requests import Session,TooManyRedirects,Timeout
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

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(api_url, params=parameters)
        return json.loads(response.text).get("data").get(symbol)
    except (ConnectionError, Timeout, TooManyRedirects) as e:

        print(e)


if __name__ == "__main__":
    result = get_latest_coin_data ("ADA")
    pprint(result)


