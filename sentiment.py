from transformers import pipeline

def analyze_sentiment(news_list):
    senti_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return [senti_pipe(news)[0] for news in news_list]
