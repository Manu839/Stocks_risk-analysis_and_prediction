from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import capm, stock_analysis, stock_prediction

app = FastAPI(
    title="Stocklyzer API",
    description="A comprehensive stock analysis and prediction API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:5174",  # Added for current Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(capm.router, prefix="/api/capm", tags=["CAPM Calculator"])
app.include_router(stock_analysis.router, prefix="/api/analysis", tags=["Stock Analysis"])
app.include_router(stock_prediction.router, prefix="/api/prediction", tags=["Stock Prediction"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Stocklyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
