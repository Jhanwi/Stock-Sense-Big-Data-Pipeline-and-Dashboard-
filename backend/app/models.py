from pydantic import BaseModel, Field
from typing import Optional, List

class PipelineTriggerRequest(BaseModel):
    ticker: str = Field(..., example="RELIANCE")
    exchange: str = Field(..., example="NSE")
    s3_bucket: str = Field(..., example="stock-sense-data-lake")

class PipelineStatusResponse(BaseModel):
    status: str
    ticker: str
    exchange: str
    message: str
    execution_time_seconds: Optional[float] = None

class HistoricalPricePoint(BaseModel):
    date: str
    open: float
    close: float
    high: float
    low: float

class StockDataSnapshot(BaseModel):
    company_name: str
    ticker: str
    ltp: Optional[float] = None
    open_price: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    market_cap_formatted: str
    historical_series: List[HistoricalPricePoint] = Field(default=[])

