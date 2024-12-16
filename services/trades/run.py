from typing import Union
from loguru import logger
from quixstreams import Application
from config import config
from src.kraken_api.mock import KrakenMockAPI
from src.kraken_api.websocket import KrakenWebsocketAPI


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: Union[KrakenWebsocketAPI, KrakenMockAPI]
):
    """
    It does 2 things:
    1. Reads trades from the Kraken API and
    2. Pushes them to a Kafka topic.

    Args:
        kafka_broker_address: str
        kafka_topic: str
        kraken_api: Union[KrakenWebsocketAPI, KrakenMockAPI]
      
    Returns:
        None
    """
    logger.info('Start the trades service')
    
    
    # Initialize the Quix Streams application.
    # This class handles all the low-level details to connect to Kafka.
    app = Application(
        broker_address=kafka_broker_address,
    )
    
    while True:
        trades = kraken_api.get_trades()

        # Define the topic where we will push the trades to
        topic = app.topic(name=kafka_topic, value_serializer="json")

        with app.get_producer() as producer:

            for trade in trades:
                # serialize the trade as bytes
                message = topic.serialize(
                    key=trade.pair,
                    value=trade.to_dict(),
                )

                # push the serialized message to the topic
                producer.produce(topic=topic.name, value=message.value, key=message.key
                                )

                logger.info(f'Pushed trade to Kafka: {trade}')


if __name__ == '__main__':
    main(
        config.kafka_broker_address,
        config.kafka_topic,
        # Mock Data for Kraken API
        kraken_api=KrakenWebsocketAPI(pairs=config.pairs)
        )