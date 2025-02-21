import time
import os
from pprint import pprint
from quixstreams import Application
from connect_API import get_crypto_data

def main():
       app = Application(broker_address="localhost:9092", consumer_group="crypto_group_cake")
       coins_topic = app.topic(name = "crypto_cake", value_serializer="json")
       with app.get_producer() as producer:
            while True:
                coin_latest = get_crypto_data()
                
               
                kafka_message_CAKE = coins_topic.serialize(
                     key= coin_latest["CAKE"]["symbol"], value=coin_latest
                )

                print(
                     f"produce event with key = {kafka_message_CAKE.key}, value = {coin_latest["CAKE"]["quote"]['USD']['price']}"
                )

                producer.produce(
                     topic=coins_topic.name, key=kafka_message_CAKE.key, value=kafka_message_CAKE.value
                )
                time.sleep(45)


if __name__ == "__main__":
    main()
