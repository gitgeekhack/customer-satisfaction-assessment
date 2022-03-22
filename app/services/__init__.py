from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.constants import model_name

sentiment_pipeline = pipeline('sentiment-analysis', model=model_name)
sid_obj = SentimentIntensityAnalyzer()
