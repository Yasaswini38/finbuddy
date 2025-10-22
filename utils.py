import yfinance as yf
import re
import pandas as pd

def fetch_stock_data(ticker):
    df = yf.download(ticker, period='6mo', interval='1d')
    return df

def fetch_top_etfs(count=10):
    tickers = ['SPY', 'IVV', 'VOO', 'VTI', 'QQQ', 'DIA', 'IWM', 'EFA', 'EEM', 'AGG']
    return tickers[:count]

def fetch_top_mutual_funds(count=5):
    tickers = ['VTSAX', 'SWPPX', 'FXAIX', 'VFIAX', 'VIGAX']
    return tickers[:count]

def extract_tickers_from_advice(advice_raw):
    tickers = set(re.findall(r"\b[A-Z]{2,5}(?:\.NS)?\b", advice_raw))
    return list(tickers)

def simple_next_day_prediction(ticker):
    try:
        df = yf.download(ticker, period="7d", interval="1d")
        # Check for DataFrame issues
        if df is None or df.empty or 'Close' not in df.columns or len(df['Close'].dropna()) < 2:
            return "N/A"
        close_series = df['Close'].dropna()
        last_close = float(close_series.iloc[-1])
        prev_close = float(close_series.iloc[-2])
        change = last_close - prev_close
        prediction = last_close + change
        low = prediction - abs(change) * 0.5
        high = prediction + abs(change) * 0.5
        usd_to_inr = 83
        prediction_inr = prediction * usd_to_inr
        low_inr = low * usd_to_inr
        high_inr = high * usd_to_inr

        return f"₹{prediction_inr:,.2f} (range: ₹{low_inr:,.2f}–₹{high_inr:,.2f})"
       
    except Exception as e:
        return f"Prediction error: {str(e)}"

