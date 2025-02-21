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
from connect_exchange import get_exchange_rates

st.set_page_config(page_title="Kryptokollen", page_icon=":bar_chart", layout="wide")

conection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
engine = create_engine(conection_string)
count = st_autorefresh(interval=1000 * 10, limit=100)

def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df.set_index('timestamp', inplace=True)
    return df


def layout():
    st.sidebar.title("Settings")
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
    with st.expander("See Dataframe"):
        def format_price(volume):
            if volume >= 1000000:
                return f"{volume / 1000000:.1f}M"
            elif volume >= 1000:
                return f"{volume / 1000:.1f}K"
            return f"{volume:.2f}"
        
        query = f"SELECT * FROM crypto;"
        df = load_data(query)
        df = df[df['symbol'] == crypto]
        df["formatted_volume"] = df["volume"].apply(format_price)
        st.dataframe(df.tail(5))
    
    price_usd = df["price_usd"]
    rates = get_exchange_rates()
    price = round(price_usd * rates[option],2)
    price_chart = line_chart(x=df.index, y=price, title="Rates")
    st.subheader("Crypto Analytics")

    col = st.columns((1,3))
    with col[0]:
        price_usd = df["price_usd"].tail(1).values[0]
        privius_usd_price = df["price_usd"].tail(2).values[0]
        rates = get_exchange_rates()
        correct_price = round(price_usd * rates[option],2)
        privius_pirce = round(privius_usd_price * rates[option],2)
        st.metric(label="Price", value=f"{correct_price}{option}",delta=f"{privius_pirce}{option}" ,border=True)
        procent_change = df["percent_change_1h"].tail(1).values[0]
        previus_change = df["percent_change_1h"].tail(2).values[0]
        st.metric(label="Price change", value=f"{procent_change:.2f}%",delta=f"{previus_change:.2f}%" ,border=True)
        st.metric(label="Volume change", value=df["volume_change"].tail(1),delta=df["volume_change"].tail(2).values[0] ,border=True)
        format_volume = format_price(df["volume"].tail(1).values[0])
        privius_volyme = format_price(df["volume"].tail(2).values[0])
        st.metric(label="Volume", value=format_volume,delta=privius_volyme,border=True)
    with col[1]:
        st.pyplot(price_chart)



if __name__ == "__main__":
    layout()
