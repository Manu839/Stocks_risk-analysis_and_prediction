from fastapi import APIRouter, HTTPException
from models.stock_models import CAPMRequest, CAPMResponse, BetaResult, CAPMResult
import pandas as pd
import yfinance as yf
import datetime
import capm_functions
from typing import List, Dict, Any

router = APIRouter()

@router.post("/calculate", response_model=CAPMResponse)
async def calculate_capm(request: CAPMRequest):
    """
    Calculate CAPM (Capital Asset Pricing Model) for selected stocks
    """
    try:
        # Set date range
        end = datetime.date.today()
        start = datetime.date(datetime.date.today().year - request.years, 
                            datetime.date.today().month, 
                            datetime.date.today().day)
        
        # Download S&P 500 data
        SP500 = yf.download("^GSPC", start=start, end=end)
        
        # Download stock data
        stocks_df = pd.DataFrame()
        for stock in request.stocks:
            try:
                data = yf.download(stock, start=start, end=end)
                stocks_df[f'{stock}'] = data['Close']
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error downloading data for {stock}: {str(e)}")
        
        stocks_df.reset_index(inplace=True)
        SP500.reset_index(inplace=True)
        
        # Process S&P 500 data
        SP500 = SP500[['Date', 'Close']].copy()
        SP500.columns = ['Date', 'GSPC']
        stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
        SP500['Date'] = pd.to_datetime(SP500['Date'])
        
        # Merge dataframes
        stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')
        
        # Convert to list of dictionaries for JSON response
        stocks_data = stocks_df.to_dict('records')
        
        # Normalize data
        normalized_df = capm_functions.normalize(stocks_df)
        normalized_data = normalized_df.to_dict('records')
        
        # Calculate daily returns
        stocks_daily_return = capm_functions.daily_return(stocks_df)
        
        # Calculate beta and alpha for each stock
        beta_results = []
        capm_results = []
        
        for stock in request.stocks:
            if stock in stocks_daily_return.columns:
                beta, alpha = capm_functions.calculate_beta(stocks_daily_return, stock)
                
                beta_results.append(BetaResult(
                    stock=stock,
                    beta=round(beta, 4),
                    alpha=round(alpha, 4)
                ))
                
                # Calculate CAPM expected return
                rf = 0  # Risk-free rate
                rm = stocks_daily_return['GSPC'].mean() * 252  # Market return
                expected_return = rf + beta * (rm - rf)
                
                capm_results.append(CAPMResult(
                    stock=stock,
                    beta=round(beta, 4),
                    expected_return=round(expected_return, 4)
                ))
        
        return CAPMResponse(
            stocks_data=stocks_data,
            normalized_data=normalized_data,
            beta_results=beta_results,
            capm_results=capm_results,
            market_return=round(stocks_daily_return['GSPC'].mean() * 252, 4),
            risk_free_rate=0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating CAPM: {str(e)}")

@router.get("/available-stocks")
async def get_available_stocks():
    """
    Get list of available stock symbols
    """
    return {
        "stocks": ["TSLA", "AAPL", "NFLX", "MSFT", "WIPRO", "INFY", "RELIANCE", "AMZN", "NVDA"],
        "description": "Popular stock symbols available for CAPM analysis"
    }
