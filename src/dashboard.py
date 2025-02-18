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

conection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

engine = create_engine(conection_string)

count = st_autorefresh(interval=1000*10, limit=100)

def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def layout():
    df = load_data("SELECT * FROM crypto;")
    st.markdown("# Kryptokollen")

    st.dataframe(df.tail())
    
    option = st.selectbox(
        "How would you like to be contacted?",
    ("SEK", "NOK", "DKK", "EUR"),
    )
    
    st.write("You selected:", option)


if __name__ == "__main__":
    layout()