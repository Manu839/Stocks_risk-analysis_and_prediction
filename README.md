# 📈 Stock Analysis and Prediction App

A full-stack web application for analyzing, evaluating, and forecasting stock performance using financial models like CAPM and ARIMA. Built with a React.js + Tailwind CSS frontend and a Flask backend.

---

## 🚀 Features

- 🔍 **Stock Data Visualization**  
  View live stock prices, volume, and trends with interactive charts.

- 📊 **Performance Analysis**  
  Analyze rolling averages, moving trends, and past performance of stocks.

- 💰 **CAPM Evaluation**  
  Predict expected return using the Capital Asset Pricing Model (CAPM).

- 📈 **Stock Price Forecasting**  
  Forecast future stock prices using ARIMA time series modeling.

- 🌐 **Modern UI**  
  Responsive and visually appealing interface using Tailwind CSS.

---

## Results 

<img width="1903" height="547" alt="Screenshot 2025-07-26 173013" src="https://github.com/user-attachments/assets/c108a66f-6001-455f-aa24-4a4df33b18d3" />

<img width="1901" height="865" alt="Screenshot 2025-07-26 172941" src="https://github.com/user-attachments/assets/2722412d-f58c-41aa-ad84-ccbc6a61b2a9" />

<img width="1908" height="682" alt="Screenshot 2025-07-26 173049" src="https://github.com/user-attachments/assets/a731146b-5496-4ff2-a23a-46cac5739cdb" />

<img width="1902" height="627" alt="Screenshot 2025-07-26 173031" src="https://github.com/user-attachments/assets/d8c66fd6-1095-4457-85f5-ff6178095e38" />


## 🛠 Tech Stack

### Frontend
- **React.js** – Component-based UI
- **Tailwind CSS** – Utility-first styling
- **Recharts** – Data visualization

### Backend
- **Flask** – Lightweight Python server
- **yfinance / pandas / numpy** – Financial data handling
- **statsmodels** – ARIMA forecasting
- **Flask-CORS** – Enable frontend-backend communication

---
## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/stock-analysis-app.git
cd stock-analysis-app
```
### 2. Backend Setup
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
### 3. Frontend Setup
```bash
cd ../client
npm install
npm run dev
```
##  🔗 API Endpoints
| Endpoint    | Method | Description                      |
| ----------- | ------ | -------------------------------- |
| `/stock`    | POST   | Get historical stock data        |
| `/capm`     | POST   | Calculate CAPM values            |
| `/forecast` | POST   | Predict future prices with ARIMA |
| `/analysis` | POST   | Run performance analysis         |

