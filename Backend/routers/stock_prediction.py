from fastapi import APIRouter, HTTPException
from models.stock_models import StockPredictionRequest, StockPredictionResponse, StockData, PredictionData
import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from typing import List

router = APIRouter()

def get_data(ticker: str) -> pd.DataFrame:
    """Get stock data from Yahoo Finance"""
    stock_data = yf.download(ticker, start='2020-01-01')
    return stock_data[['Close']]

def stationary_check(close_price: pd.Series) -> float:
    """Check if the time series is stationary using ADF test"""
    adf_test = adfuller(close_price.dropna())
    return round(adf_test[1], 3)

def get_rolling_mean(close_price: pd.DataFrame) -> pd.DataFrame:
    """Calculate 7-day rolling mean of closing prices"""
    if isinstance(close_price, pd.DataFrame):
        close_price = close_price['Close']
    rolling_price = close_price.rolling(window=7).mean().dropna()
    if not isinstance(rolling_price, pd.DataFrame):
        rolling_price = rolling_price.to_frame(name='Close')
    return rolling_price

def get_differencing_order(close_price: pd.DataFrame) -> int:
    """Determine optimal differencing order for stationarity"""
    if isinstance(close_price, pd.DataFrame):
        close_price = close_price['Close'].copy()
    p_value = stationary_check(close_price)
    d = 0
    while p_value > 0.05 and d < 2:
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_check(close_price)
    return d

def fit_model(data: np.ndarray, differencing_order: int, steps: int = 30) -> np.ndarray:
    """Fit ARIMA model and generate forecasts"""
    model = ARIMA(data, order=(5, differencing_order, 1))
    model_fit = model.fit()
    forecast = model_fit.get_forecast(steps=steps)
    return forecast.predicted_mean

def evaluate_model(original_price: np.ndarray, differencing_order: int) -> float:
    """Evaluate ARIMA model using RMSE on test data"""
    if len(original_price) < 60:  # Need enough data for train/test split
        return 0.0
    
    train_data = original_price[:-30]
    test_data = original_price[-30:]
    predictions = fit_model(train_data, differencing_order, steps=30)
    
    # Ensure same length for RMSE calculation
    min_len = min(len(test_data), len(predictions))
    rmse = np.sqrt(mean_squared_error(test_data[:min_len], predictions[:min_len]))
    return round(rmse, 2)

def scaling(close_price: pd.DataFrame):
    """Scale the data using StandardScaler"""
    scaler = StandardScaler()
    if isinstance(close_price, pd.DataFrame):
        close_price = close_price['Close'].values
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data.flatten(), scaler

def get_forecast(scaled_data: np.ndarray, original_price_df: pd.DataFrame, 
                differencing_order: int, forecast_steps: int = 30) -> pd.DataFrame:
    """Generate forecast using ARIMA model"""
    model = ARIMA(scaled_data, order=(5, differencing_order, 1))
    model_fit = model.fit()
    forecast = model_fit.get_forecast(steps=forecast_steps)
    predictions = forecast.predicted_mean
    
    last_date = original_price_df.index[-1]
    forecast_index = pd.date_range(start=last_date + timedelta(days=1), 
                                 periods=forecast_steps, freq='D')
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=['Close'])
    return forecast_df

def inverse_scaling(scaler: StandardScaler, scaled_data) -> np.ndarray:
    """Inverse transform scaled data back to original scale"""
    if isinstance(scaled_data, (pd.Series, pd.DataFrame)):
        scaled_data = scaled_data.values
    return scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1)).flatten()

@router.post("/predict", response_model=StockPredictionResponse)
async def predict_stock(request: StockPredictionRequest):
    """
    Predict stock prices using ARIMA model
    """
    try:
        # Get historical data
        close_price = get_data(request.symbol)
        
        if close_price.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {request.symbol}")
        
        # Convert historical data to StockData format
        historical_data = []
        for date, row in close_price.iterrows():
            historical_data.append(StockData(
                date=date.strftime('%Y-%m-%d'),
                price=round(row['Close'], 2)
            ))
        
        # Calculate rolling mean
        rolling_price = get_rolling_mean(close_price)
        
        # Ensure 'Close' column exists
        if 'Close' not in rolling_price.columns:
            if len(rolling_price.columns) == 1:
                rolling_price.columns = ['Close']
            else:
                raise HTTPException(status_code=500, detail="Unable to process price data")
        
        # Get differencing order for stationarity
        differencing_order = get_differencing_order(rolling_price)
        
        # Scale the data
        scaled_data, scaler = scaling(rolling_price)
        
        # Evaluate model performance
        rmse = evaluate_model(scaled_data, differencing_order)
        
        # Generate forecast
        forecast = get_forecast(scaled_data, rolling_price, differencing_order, request.days)
        
        # Inverse scale the forecast
        forecast_values = inverse_scaling(scaler, forecast['Close'])
        forecast['Close'] = forecast_values

        # Convert forecast to PredictionData format
        predictions = []
        for i, (date, row) in enumerate(forecast.iterrows()):
            predictions.append(PredictionData(
                date=date.strftime('%Y-%m-%d'),
                predicted_price=round(float(forecast_values[i]), 2)
            ))
        
        # Model information
        model_info = {
            "model_type": "ARIMA",
            "order": f"(5, {differencing_order}, 1)",
            "rmse": float(rmse),
            "forecast_days": request.days,
            "data_points_used": len(rolling_price),
            "last_actual_price": round(float(close_price['Close'].iloc[-1]), 2),
            "first_predicted_price": round(float(forecast_values[0]), 2) if len(forecast_values) > 0 else None,
            "stationarity_achieved": differencing_order <= 2
        }
        
        return StockPredictionResponse(
            symbol=request.symbol.upper(),
            historical_data=historical_data[-60:],  # Return last 60 days for context
            predictions=predictions,
            model_info=model_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting stock {request.symbol}: {str(e)}")

@router.get("/model-info")
async def get_model_info():
    """
    Get information about the prediction model
    """
    return {
        "model_type": "ARIMA (AutoRegressive Integrated Moving Average)",
        "description": "A statistical model used for time series forecasting that combines autoregression, differencing, and moving averages",
        "parameters": {
            "p": 5,  # Autoregressive order
            "d": "Auto-determined",  # Differencing order (0-2)
            "q": 1   # Moving average order
        },
        "features": [
            "Automatic stationarity testing using ADF test",
            "7-day rolling mean smoothing",
            "Data scaling for improved model performance",
            "RMSE evaluation for model accuracy",
            "Configurable forecast horizon (default: 30 days)"
        ],
        "limitations": [
            "Assumes historical patterns will continue",
            "May not capture sudden market changes or external events",
            "Accuracy decreases with longer forecast horizons",
            "Requires sufficient historical data (minimum 60 days recommended)"
        ]
    }
