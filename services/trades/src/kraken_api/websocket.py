import json
from datetime import datetime
from typing import List

from loguru import logger
from websocket import create_connection

from .trade import Trade


class KrakenWebsocketAPI:
    """
    Websocket API for Kraken
    pairs: list of the pairs to connect websocket
    URL: Kraken wosocket connection URL
    """

    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        # create a websocket client
        self._ws_client = create_connection(self.URL)

        # subcribe to websocket
        self._subscribe()

    def get_trades(self) -> List[Trade]:
        """
        Extract the trade data from krakenAPI
        """
        # receive the data from the websocket
        data = self._ws_client.recv()

        # when data not presentwebsocket sent an hearbeat instead of data
        if 'heartbeat' in data:
            logger.info('Heartbeat received')
            return []

        # transform raw string into a JSON object
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')
            return []

        try:
            trades_data = data['data']
        except KeyError as e:
            logger.error(f'No `data` field with trades in the message {e}')
            return []

        trades = [
            Trade(
                pair=trade['symbol'],
                price=trade['price'],
                volume=trade['qty'],
                timestamp=trade['timestamp'],
                timestamp_ms=self.datetime2milisec(trade['timestamp']),
            )
            for trade in trades_data
        ]
        return trades

    def datetime2milisec(self, iso_time: str) -> int:
        """ "
        Convert the iso_time to Unix miliseconds

        Args:
            iso_str: str
        """
        dt = datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        return int(dt.timestamp() * 1000)

    def _subscribe(self):
        """ "
        Connecting kraken Websocket API
        skip the confirmation to received data
        """
        self._ws_client.send(
            json.dumps(
                {
                    'method': 'subscribe',
                    'params': {
                        'channel': 'trade',
                        'symbol': ['MATIC/USD'],
                        'snapshot': False,
                    },
                }
            )
        )
        for _ in self.pairs:
            self._ws_client.recv()
            self._ws_client.recv()
