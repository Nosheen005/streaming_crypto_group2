import requests

def get_exchange_rates(): 
        EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD" 
        response = requests.get(EXCHANGE_RATE_API_URL) 
        response.raise_for_status()
        data = response.json() 
        
        rates = { "SEK": data["rates"]["SEK"], 
                 "NOK": data["rates"]["NOK"], 
                 "DKK": data["rates"]["DKK"], 
                 "EUR": data["rates"]["EUR"]
        } 
        return rates
