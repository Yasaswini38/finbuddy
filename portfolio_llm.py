import os
from mistralai.client import MistralClient

def recommend_portfolio(user_profile, stock_data, news_sentiment):
    api_key = os.environ["MISTRAL_API_KEY"]
    client = MistralClient(api_key=api_key)
    model_name = "mistral-large-latest" 

    prompt = f"""
            You are an expert, conservative, trustworthy, and empathetic financial planner for Indian and US investors. When you answer, organize the advice in visually segmented sections with: block-style bold headlines, lists, cards, and tables (not raw paragraphs).

            User Profile: {user_profile}

            Recent Market Data: {stock_data}
            Market Sentiment: {news_sentiment}

            1. Recommend specific mutual funds, ETFs, AND **list 2-3 individual stocks** (with US and Indian tickers if possible) that are appropriate for the user's profile.
            2. For each stock, provide a 1-day price prediction (based on most recent market data) with a confidence interval, label it "Next Day Prediction", and cite reasoning in one or two sentences.
            3. Make sure all advice (funds, ETFs, stocks) is simple, actionable, and formatted in block-style output for a web dashboard. Use markdown syntax for lists and tables.
            4. Clearly show an overall sample portfolio allocation in a markdown table.
            5. End with a "Final Advice Block" (1–4 actionable tips) based on major risks or opportunities from the latest data.

            DO NOT use paragraphs or prose—use only well-structured, labeled blocks, tables, and bullet points.

            Data for context:
            {stock_data}

            """

    response = client.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content