from datetime import datetime
from typing import List, Tuple

import requests
from config import cryptopanic_credentials
from loguru import logger
from pydantic import BaseModel


class News(BaseModel):
    """
    News response model for cryptopanic API.
    """

    title: str
    published_at: str
    source: str

    def to_dict(self) -> dict:
        return {
            **self.model_dump(),
            'timestamp_ms': int(
                datetime.fromisoformat(
                    self.published_at.replace('Z', '+00:00')
                ).timestamp()
                * 1000
            ),
        }


class NewsDownloader:
    """ "
    News downloader from the cryptopanic website

    """

    URL = 'https://cryptopanic.com/api/free/v1/posts/'

    def __init__(self, crtptopanic_api_key: str):
        self.crtptopanic_api_key = crtptopanic_api_key

    def get_news(self) -> List[News]:
        """
        Get the news from the cryptopanic website REST API.

        Returns:
            News: News response model for cryptopanic API.
        """
        url = self.URL + '?auth_token=' + self.crtptopanic_api_key
        try:
            news = []
            while True:
                # Get the batch of news
                batch_news, next_url = self.get_batch_of_news(url)
                logger.info(f'Fetching news from {url}')
                logger.info(f'Got {len(batch_news)} news')

                # Append the batch news to the news list
                news += batch_news

                # Check if there are more news to fetch
                if not batch_news:
                    break

                if not next_url:
                    break

                # Update the url to fetch the next batch of news
                url = next_url

        except Exception as e:
            logger.error(f'Error while fetching news: {e}')
            return None

        news.sort(key=lambda x: x.published_at, reverse=False)
        return news

    def get_batch_of_news(self, url: str) -> Tuple[List[News], str]:
        """
        Get the news from the cryptopanic website REST API.

        Returns:
            News: News response model for cryptopanic API.
        """
        try:
            response = requests.get(url)
            response = response.json()

        except Exception as e:
            logger.error(f'Error while fetching news: {e}')
            return ([], '')

        news = [
            News(
                title=post['title'],
                published_at=post['published_at'],
                source=post['domain'],
            )
            for post in response['results']
        ]

        next_page = response['next']
        return (news, next_page)


if __name__ == '__main__':
    news_downloader = NewsDownloader(cryptopanic_credentials.api_key)
    news = news_downloader.get_news()
