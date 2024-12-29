from loguru import logger
from news_data_source import NewsDataSource
from news_downloader import NewsDownloader
from quixstreams import Application


def main(kafka_broker_address: str, kafka_topic: str, input_source: NewsDataSource):
    """
    2 main function to run the news data source.
    1.download the news from the cryptopanic website.
    2. produce the news to the kafka topic.

    Args:
        kafka_broker_address: str: The kafka broker address
        kafka_topic: str: The kafka topic
        input_source: NewsDataSource: The news data source object

    Returns:
        None
    """
    logger.info('Starting news service')

    # Initialize the Quix Streams application.
    app = Application(broker_address=kafka_broker_address)

    # Define the topic where we will push the news to
    output_topic = app.topic(name=kafka_topic, value_serializer='json')

    # Start the news data source
    sdf = app.dataframe(source=news_data_source)

    # print the news to the console
    sdf.print(metadata=True)

    # Push the news to the kafka topic
    sdf.to_topic(output_topic)

    # Run the application
    app.run()


if __name__ == '__main__':
    from config import config, cryptopanic_credentials

    # Define New downloader object
    news_downloader = NewsDownloader(cryptopanic_credentials.api_key)

    # Define the news data source object
    news_data_source = NewsDataSource(news_downloader, config.polling_interval_sec)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        input_source=news_data_source,
    )
