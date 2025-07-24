import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 30000, // 30 seconds timeout for long-running predictions
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// CAPM Calculator API
export const capmAPI = {
  calculate: async (stocks, years = 1) => {
    try {
      const response = await api.post('/capm/calculate', {
        stocks,
        years
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to calculate CAPM')
    }
  }
}

// Stock Analysis API
export const stockAnalysisAPI = {
  analyze: async (symbol, period = '1y') => {
    try {
      const response = await api.post('/analysis/analyze', {
        symbol,
        period
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to analyze stock')
    }
  }
}

// Stock Prediction API
export const stockPredictionAPI = {
  predict: async (symbol, days = 30) => {
    try {
      const response = await api.post('/prediction/predict', {
        symbol,
        days
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to predict stock prices')
    }
  }
}

// Health check API
export const healthAPI = {
  check: async () => {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      throw new Error('Backend service is not available')
    }
  }
}

// Utility function to validate stock symbols
export const validateStockSymbol = (symbol) => {
  if (!symbol || typeof symbol !== 'string') {
    return false
  }
  // Basic validation: 1-5 characters, letters only
  const symbolRegex = /^[A-Za-z]{1,5}$/
  return symbolRegex.test(symbol.trim())
}

// Utility function to format stock symbols
export const formatStockSymbol = (symbol) => {
  return symbol.trim().toUpperCase()
}

// Common stock symbols for suggestions
export const popularStocks = [
  { symbol: 'AAPL', name: 'Apple Inc.' },
  { symbol: 'GOOGL', name: 'Alphabet Inc.' },
  { symbol: 'MSFT', name: 'Microsoft Corporation' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.' },
  { symbol: 'TSLA', name: 'Tesla Inc.' },
  { symbol: 'META', name: 'Meta Platforms Inc.' },
  { symbol: 'NVDA', name: 'NVIDIA Corporation' },
  { symbol: 'NFLX', name: 'Netflix Inc.' },
  { symbol: 'AMD', name: 'Advanced Micro Devices' },
  { symbol: 'INTC', name: 'Intel Corporation' }
]

export default api
