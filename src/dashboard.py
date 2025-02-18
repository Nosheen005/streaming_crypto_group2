import streamlit as st
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from sqlalchemy import create_engine
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from charts import line_chart
import requests

st.set_page_config(page_title="Kryptokollen", page_icon=":bar_chart", layout="wide")

conection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

engine = create_engine(conection_string)

count = st_autorefresh(interval=1000*10, limit=100)

def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def layout():
    #st.set_page_config(page_title="Kryptokollen", page_icon=":bar_chart", layout="wide")
    
    st.sidebar.title("Home")
    st.title("Kryptokollen")
    
    crypto = st.sidebar.selectbox(
    "Choose crypto",
    ("ADA", "CAKE"),
    )
    st.sidebar.write("You selected:", crypto)

    option = st.sidebar.selectbox(
    "Choose currency",
    ("SEK", "NOK", "DKK", "EUR"),
    )

    st.sidebar.write("You selected:", option)


    df = load_data("SELECT * FROM crypto;")
    

    st.dataframe(df.tail())

    def format_large_number(value):
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.1f}B"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value / 1_000:.1f}K"
        return f"{value:.2f}"
    
    price_usd = df["price_usd"]

    st.write("You selected:", option)

    
    EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD" 

    def get_exchange_rates(): 
        response = requests.get(EXCHANGE_RATE_API_URL) 
        response.raise_for_status()
        data = response.json() 
        
        rates = { "SEK": data["rates"]["SEK"], 
                 "NOK": data["rates"]["NOK"], 
                 "DKK": data["rates"]["DKK"], 
                 "EUR": data["rates"]["EUR"]
        } 
        return rates
    
    rates = get_exchange_rates()
    price = 0

    if option == "SEK":
        price = round(price_usd*rates["SEK"],2)
    elif option == "NOK":
        price = round(price_usd*rates["NOK"],2)
    elif option == "DKK":
        price = round(price_usd*rates["DKK"],2)
    elif option == "EUR":
        price = round(price_usd*rates["EUR"],2)
    else:
        price_sek,price_nok,price_dkk,price_eur = None,None,None,None
    
    price_chart = line_chart(x=df.index, y=price, title="Rates")
    
    st.metric("Cardano",df["price_usd"].tail(1))
    st.pyplot(price_chart)


if __name__ == "__main__":
    layout()