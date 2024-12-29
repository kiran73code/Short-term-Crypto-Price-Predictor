import time
from typing import Optional

from news_downloader import NewsDownloader
from quixstreams.sources.base import StatefulSource


class NewsDataSource(StatefulSource):
    """
    get the news from cryptopanic website and produce it to the kafka topic.
    """

    def __init__(
        self, news_downloader: NewsDownloader, polling_interval_sec: Optional[int] = 10
    ):
        """ "
        news_downloader: NewsDownloader: The news downloader object to get news
        polling_interval_sec: int: The polling interval in seconds
        """
        self.news_downloader = news_downloader
        self.polling_interval_sec = polling_interval_sec
        super().__init__(name='news_data_source')

    def run(self):
        last_published_at = self.state.get('published_at', None)
        while self.running:
            # Download news from cryptopanix website and out put is sorted incresing order published at
            news = self.news_downloader.get_news()

            if last_published_at:
                news = [
                    news_item
                    for news_item in news
                    if news_item.published_at > last_published_at
                ]

            if news:
                for news_item in news:
                    # Serialize the news item to dict and produce it to the kafka topic
                    message = self.serialize(key='news', value=news_item.to_dict())

                    # Produce the news to the kafka topic
                    self.produce(key=message.key, value=message.value)

            # Update the last published at time news item sorted in increasing order
            if news:
                last_published_at = news[-1].published_at

            # Update the last published at time news item sorted in increasing order
            self.state.set(
                'published_at', last_published_at
            )  # Use set method to update state

            # Flush the state changes it's commit the state changes
            self.flush()

            # polling interval
            time.sleep(self.polling_interval_sec)
