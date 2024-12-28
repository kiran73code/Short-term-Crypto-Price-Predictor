from typing import Literal

from candle import update_candles
from config import Config
from loguru import logger
from quixstreams import Application
from technical_indicators import compute_indicators


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    max_candles_in_state: int,
    candle_seconds: int,
    data_source: Literal['live', 'historical', 'test'],
):
    """
    3 Steps
    1.Ingest candle topic data from Kafka
    2.Compute technical indicators
    3.Publish the computed technical indicators to a ntechnical-indicatorw Kafka topic

    Args:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic
        kafka_output_topic (str): Kafka output topic
        kafka_consumer_group (str): Kafka consumer group
        max_candles_in_state: The maximum number of candles to keep in the state
        candle_seconds: The number of seconds per candle
        data_source: The data source (live, historical, test)
    Returns:
        None
    """
    logger.info('Hello from technical-indicators!')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='latest' if data_source == 'live' else 'earliest',
    )

    # Define the input and output topics of our streaming application
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
    )
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json',
    )
    # Create a Streaming DataFrame so we can start transforming data in real time
    sdf = app.dataframe(topic=input_topic)

    # We only keep the candles with the same window size as the candle_seconds

    sdf = sdf[sdf['candle_seconds'] == candle_seconds]

    # Update the list of candles in the state
    sdf = sdf.apply(update_candles, stateful=True)

    # Compute the technical indicators from the candles in the state
    sdf = sdf.apply(compute_indicators, stateful=True)

    # Add a `coin` field to the final message
    sdf = sdf.apply(lambda value: {**value, 'coin': value['pair'].split('/')[0]})

    sdf = sdf.update(lambda value: logger.debug(f'Final message: {value}'))

    # Send the final messages to the output topic
    sdf = sdf.to_topic(output_topic)
    print('done')
    app.run()


if __name__ == '__main__':
    config = Config()
    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        max_candles_in_state=config.max_candles_in_state,
        candle_seconds=config.candle_seconds,
        data_source=config.data_source,
    )
