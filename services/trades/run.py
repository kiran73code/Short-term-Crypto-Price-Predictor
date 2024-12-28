from config import config
from loguru import logger
from quixstreams import Application
from src.kraken_api.base import TradesAPI
from src.kraken_api.mock import KrakenMockAPI
from src.kraken_api.rest import KrakenRestAPI
from src.kraken_api.websocket import KrakenWebsocketAPI


def main(kafka_broker_address: str, kafka_topic: str, trades_api: TradesAPI):
    """
    It does 2 things:
    1. Reads trades from the Kraken API and
    2. Pushes them to a Kafka topic.

    Args:
        kafka_broker_address: str
        kafka_topic: str
        trades_api: Union[KrakenWebsocketAPI, KrakenMockAPI]

    Returns:
        None
    """
    logger.info('Start the trades service')

    # Initialize the Quix Streams application.
    # This class handles all the low-level details to connect to Kafka.
    app = Application(
        broker_address=kafka_broker_address,
    )

    while not trades_api.is_done():
        trades = kraken_api.get_trades()

        # Define the topic where we will push the trades to
        topic = app.topic(name=kafka_topic, value_serializer='json')

        with app.get_producer() as producer:
            for trade in trades:
                # serialize the trade as bytes
                message = topic.serialize(
                    key=trade.pair.replace('/', '-'),
                    value=trade.to_dict(),
                )

                # push the serialized message to the topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Pushed trade to Kafka: {trade}')


if __name__ == '__main__':
    # Initialize the Kraken API depending on the data source
    if config.data_source == 'live':
        kraken_api = KrakenWebsocketAPI(pairs=config.pairs)
    elif config.data_source == 'historical':
        kraken_api = KrakenRestAPI(pairs=config.pairs, last_n_days=config.last_n_days)

    elif config.data_source == 'test':
        kraken_api = KrakenMockAPI(pairs=config.pairs)
    else:
        raise ValueError(f'Invalid data source: {config.data_source}')

    main(
        config.kafka_broker_address,
        config.kafka_topic,
        # Mock Data for Kraken API
        trades_api=kraken_api,
    )
