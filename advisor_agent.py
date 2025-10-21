import re
from utils import fetch_top_etfs, fetch_top_mutual_funds, fetch_stock_data
from sentiment import analyze_sentiment
from portfolio_llm import recommend_portfolio
import markdown
from utils import simple_next_day_prediction, extract_tickers_from_advice


def run_advisor(goal, risk_level, spending_pattern):
    etfs = fetch_top_etfs()
    mfs = fetch_top_mutual_funds()
    sample_news = [
        "Stock markets rallied amid optimism about inflation.",
        "Tech sector faces pressure after rate changes.",
        "Investors are confident in diversified ETFs."
    ]
    news_sent = analyze_sentiment(sample_news)
    stock_data = {t: fetch_stock_data(t).tail(1).to_dict() for t in etfs}
    user_profile = {
        "goal": goal,
        "risk": risk_level,
        "spending": spending_pattern
    }
    advice_raw = recommend_portfolio(user_profile, stock_data, news_sent)
    print(advice_raw) 
    tickers = extract_tickers_from_advice(advice_raw)
    stock_predictions = {ticker: simple_next_day_prediction(ticker) for ticker in tickers}
    print("Ticker Predictions:", stock_predictions)
    return advice_raw,stock_predictions
    
def format_advice_blocks(advice_raw, profile):
    profile_html = f"""
    <div class='advice-card'>
        <h3 style='color:#ffbcaf'>Profile Overview</h3>
        <ul>
            <li><b>Goal:</b> <span style='color:#f8b500'>{profile['goal']}</span></li>
            <li><b>Risk Level:</b> <span style='color:#f8b500'>{profile['risk']}</span></li>
            <li><b>Spending Style:</b> <span style='color:#f8b500'>{profile['spending']}</span></li>
        </ul>
    </div>
    """
    # Convert markdown (the rest of the LLM response) to HTML safely
    html_blocks = markdown.markdown(
        advice_raw,
        extensions=["tables", "sane_lists"]
    )
    # Combine your cute profile card with the converted sections
    return profile_html + html_blocks