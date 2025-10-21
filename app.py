from flask import Flask, render_template, request
from advisor_agent import run_advisor, format_advice_blocks
from utils import simple_next_day_prediction
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    stock_predictions = None
    single_prediction = None
    single_ticker = None

    if request.method == 'POST':
        # Stock prediction was requested
        if 'ticker' in request.form and request.form.get('ticker', '').strip():
            ticker = request.form.get('ticker', '').upper().strip()
            single_prediction = simple_next_day_prediction(ticker)
            if str(single_prediction).startswith("N/A"):
                single_prediction = None
            single_ticker = ticker
        # Advice was requested
        else:
            goal = request.form.get('goal')
            risk = request.form.get('risk')
            spending = request.form.get('spending')
            if goal and risk and spending:
                user_profile = {"goal": goal, "risk": risk, "spending": spending}
                advice_raw, stock_predictions = run_advisor(goal, risk, spending)
                stock_predictions = {t: p for t, p in stock_predictions.items() if not str(p).startswith("N/A")}
                result = format_advice_blocks(advice_raw, user_profile)

    return render_template('index.html',
                           result=result,
                           stock_predictions=stock_predictions,
                           single_prediction=single_prediction,
                           single_ticker=single_ticker
    )

if __name__ == '__main__':
    app.run(debug=True)
