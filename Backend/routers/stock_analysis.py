from fastapi import APIRouter, HTTPException
from models.stock_models import StockAnalysisRequest, StockAnalysisResponse, StockData
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/analyze", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    """
    Perform comprehensive stock analysis including price data and technical indicators
    """
    try:
        # Get stock data
        ticker = yf.Ticker(request.symbol)
        hist_data = ticker.history(period=request.period)
        stock_info = ticker.info
        
        if hist_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {request.symbol}")
        
        # Convert price data to list of StockData objects
        price_data = []
        for date, row in hist_data.iterrows():
            price_data.append(StockData(
                date=date.strftime('%Y-%m-%d'),
                price=round(row['Close'], 2)
            ))
        
        # Calculate technical indicators
        close_prices = hist_data['Close']
        
        # Moving averages
        ma_10 = close_prices.rolling(window=10).mean()
        ma_20 = close_prices.rolling(window=20).mean()
        ma_50 = close_prices.rolling(window=50).mean()
        
        # RSI calculation
        def calculate_rsi(prices, window=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        
        rsi = calculate_rsi(close_prices)
        
        # MACD calculation
        exp1 = close_prices.ewm(span=12).mean()
        exp2 = close_prices.ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        
        # Bollinger Bands
        bb_period = 20
        bb_std = 2
        bb_middle = close_prices.rolling(window=bb_period).mean()
        bb_std_dev = close_prices.rolling(window=bb_period).std()
        bb_upper = bb_middle + (bb_std_dev * bb_std)
        bb_lower = bb_middle - (bb_std_dev * bb_std)
        
        # Volume analysis
        avg_volume = hist_data['Volume'].mean()
        current_volume = hist_data['Volume'].iloc[-1]
        
        technical_indicators = {
            "moving_averages": {
                "ma_10": round(ma_10.iloc[-1], 2) if not pd.isna(ma_10.iloc[-1]) else None,
                "ma_20": round(ma_20.iloc[-1], 2) if not pd.isna(ma_20.iloc[-1]) else None,
                "ma_50": round(ma_50.iloc[-1], 2) if not pd.isna(ma_50.iloc[-1]) else None,
            },
            "rsi": round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else None,
            "macd": {
                "macd": round(macd.iloc[-1], 4) if not pd.isna(macd.iloc[-1]) else None,
                "signal": round(signal.iloc[-1], 4) if not pd.isna(signal.iloc[-1]) else None,
                "histogram": round((macd - signal).iloc[-1], 4) if not pd.isna((macd - signal).iloc[-1]) else None,
            },
            "bollinger_bands": {
                "upper": round(bb_upper.iloc[-1], 2) if not pd.isna(bb_upper.iloc[-1]) else None,
                "middle": round(bb_middle.iloc[-1], 2) if not pd.isna(bb_middle.iloc[-1]) else None,
                "lower": round(bb_lower.iloc[-1], 2) if not pd.isna(bb_lower.iloc[-1]) else None,
            },
            "volume": {
                "current": int(current_volume),
                "average": int(avg_volume),
                "relative": round(current_volume / avg_volume, 2) if avg_volume > 0 else None,
            }
        }
        
        # Calculate summary statistics
        current_price = close_prices.iloc[-1]
        previous_close = close_prices.iloc[-2] if len(close_prices) > 1 else current_price
        price_change = current_price - previous_close
        percent_change = (price_change / previous_close) * 100 if previous_close != 0 else 0
        
        high_52w = close_prices.max()
        low_52w = close_prices.min()
        avg_price = close_prices.mean()
        volatility = close_prices.std() / avg_price if avg_price > 0 else 0
        
        summary = {
            "current_price": round(current_price, 2),
            "price_change": round(price_change, 2),
            "percent_change": round(percent_change, 2),
            "high_52w": round(high_52w, 2),
            "low_52w": round(low_52w, 2),
            "average_price": round(avg_price, 2),
            "volatility": round(volatility, 4),
            "trend": "uptrend" if current_price > close_prices.iloc[0] else "downtrend",
            "market_cap": stock_info.get('marketCap'),
            "pe_ratio": stock_info.get('trailingPE'),
            "beta": stock_info.get('beta'),
            "eps": stock_info.get('trailingEps'),
        }
        
        return StockAnalysisResponse(
            symbol=request.symbol.upper(),
            current_price=round(current_price, 2),
            price_data=price_data,
            technical_indicators=technical_indicators,
            summary=summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing stock {request.symbol}: {str(e)}")

@router.get("/search/{query}")
async def search_stocks(query: str):
    """
    Search for stocks by company name or symbol
    """
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="Yahoo Finance search temporarily unavailable")
        
        data = response.json()
        results = data.get("quotes", [])
        stocks = [r for r in results if r.get("quoteType") == "EQUITY"]
        
        formatted_results = []
        for stock in stocks[:10]:  # Limit to 10 results
            formatted_results.append({
                "symbol": stock.get("symbol", ""),
                "name": stock.get("shortname", stock.get("longname", "")),
                "exchange": stock.get("exchange", ""),
                "type": stock.get("quoteType", "")
            })
        
        return {"results": formatted_results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching stocks: {str(e)}")

@router.get("/info/{symbol}")
async def get_stock_info(symbol: str):
    """
    Get detailed stock information
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            "symbol": symbol.upper(),
            "name": info.get("longName", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "website": info.get("website", ""),
            "business_summary": info.get("longBusinessSummary", ""),
            "employees": info.get("fullTimeEmployees"),
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "profit_margins": info.get("profitMargins"),
            "operating_margins": info.get("operatingMargins"),
            "return_on_assets": info.get("returnOnAssets"),
            "return_on_equity": info.get("returnOnEquity"),
            "revenue_per_share": info.get("revenuePerShare"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "beta": info.get("beta"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "dividend_yield": info.get("dividendYield"),
            "payout_ratio": info.get("payoutRatio"),
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stock info for {symbol}: {str(e)}")
