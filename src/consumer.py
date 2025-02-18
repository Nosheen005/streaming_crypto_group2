from quixstreams import Application
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from quixstreams.sinks.community.postgresql import PostgreSQLSink

def extract_coin_data(message):
    latest_quote = message["quote"]["USD"]
    return{
        "coin": message["name"],
        "price_usd": latest_quote["price"],
        "volume": latest_quote["volume_24h"],
        "updated": message["last_updated"],
        "percent_change_1h": latest_quote["percent_change_1h"]
    }

def create_postgres_sink():
    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="crypto",
        schema_auto_update=True
    )
    return sink

def main():
    app = Application(broker_address="localhost:9092", consumer_group="crypto_group", auto_offset_reset="earliest")
    crypto_topic = app.topic(name="crypto", value_deserializer="json")
    sdf = app.dataframe(topic=crypto_topic)

    sdf = sdf.apply(extract_coin_data)
    sdf.update(lambda crypto_data: print(crypto_data))

    postgres_sink = create_postgres_sink()
    sdf.sink(postgres_sink)

    app.run()

if __name__ == '__main__':
    main()