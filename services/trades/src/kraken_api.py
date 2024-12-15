"""
MOCKING The KRAKEN API Response
"""

from datetime import datetime
from time import sleep
from typing import List
from pydantic import BaseModel


class Trade(BaseModel):
    """
    SAMPLE WEBSOCKET API trade data 
        "symbol": "MATIC/USD",
        "side": "buy",
        "price": 0.5147,
        "qty": 6423.46326,
        "ord_type": "limit",
        "trade_id": 4665846,
        "timestamp": "2023-09-25T07:48:36.925533Z"
    """
    pair: str
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: int
    
    def to_dict(self) -> dict:
        """
        return the dictionary
        datetime not serializable
        """
        return {
            "pair": self.pair,
            "price": self.price,
            "volume": self.volume,
            "timestamp_ms": self.timestamp_ms
            }
    
    
class KrakenMockAPI:
    """
    MOCK data for kraken API
    """
    
    def __init__(self, pair: str):
        self.pair = pair
        
    def get_trades(self) -> List[Trade]:
        """return mocked trades"""
        mock_trades = [
            Trade(
                pair=self.pair,
                price=0.5117,
                volume=40.0,
                timestamp=datetime(2023, 9, 25, 7, 49, 37, 708706),
                timestamp_ms=172719357708706,
            ),
            Trade(
                pair=self.pair,
                price=0.5317,
                volume=40.0,
                timestamp=datetime(2023, 9, 25, 7, 49, 37, 708706),
                timestamp_ms=172719357708706,
                ),
            ]

        sleep(1)

        return mock_trades
    