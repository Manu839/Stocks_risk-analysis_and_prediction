from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date

class StockRequest(BaseModel):
    stocks: List[str]
    years: int = 1

class CAPMRequest(StockRequest):
    pass

class StockAnalysisRequest(BaseModel):
    symbol: str
    period: str = "1y"  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

class StockPredictionRequest(BaseModel):
    symbol: str
    days: int = 30

class StockData(BaseModel):
    date: str
    price: float

class BetaResult(BaseModel):
    stock: str
    beta: float
    alpha: float

class CAPMResult(BaseModel):
    stock: str
    beta: float
    expected_return: float

class CAPMResponse(BaseModel):
    stocks_data: List[Dict[str, Any]]
    normalized_data: List[Dict[str, Any]]
    beta_results: List[BetaResult]
    capm_results: List[CAPMResult]
    market_return: float
    risk_free_rate: float

class StockAnalysisResponse(BaseModel):
    symbol: str
    current_price: float
    price_data: List[StockData]
    technical_indicators: Dict[str, Any]
    summary: Dict[str, Any]

class PredictionData(BaseModel):
    date: str
    predicted_price: float
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None

class StockPredictionResponse(BaseModel):
    symbol: str
    historical_data: List[StockData]
    predictions: List[PredictionData]
    model_info: Dict[str, Any]
