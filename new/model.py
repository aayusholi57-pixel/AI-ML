from transformers import pipeline

def predict_sentiment(user_query):
    clf=pipeline("sentiment-analysis")
    output = clf(user_query)
    return output
