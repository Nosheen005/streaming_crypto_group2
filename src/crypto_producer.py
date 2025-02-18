import time
import os
from pprint import pprint
from quixstreams import Application
from connect_API import get_latest_coin_data

def main():
       app = Application(broker_address="localhost:9092", consumer_group="crypto_group")
       coins_topic = app.topic(name = "crypto", value_serializer="json")
       with app.get_producer() as producer:
            while True:
                coin_latest = get_latest_coin_data()

                kafka_message = coins_topic.serialize(
                    key=coin_latest["symbol"], value=coin_latest
                )

                print(
                    f"produce event with key = {kafka_message.key}, value = {coin_latest['quote']['USD']['price']}"
                )
                producer.produce(
                    topic=coins_topic.name, key=kafka_message.key, value=kafka_message.value
                )

                time.sleep(45)


if __name__ == "__main__":
    main()
