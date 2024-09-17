from flask import Flask, request, render_template, jsonify
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import random
from transformers import pipeline


class TextAnalysis:
    @staticmethod
    def analyze_sentiment(text):
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)
            
        compound_score = sentiment_scores['compound']
            
        if compound_score >= 0.05:
                return "Positive", abs(compound_score) * 100
        elif compound_score <= -0.05:
                return "Negative", abs(compound_score) * 100
        else:
                return "Neutral", (1 - abs(compound_score)) * 100
    