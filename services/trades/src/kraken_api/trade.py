from datetime import datetime
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
