from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    
    if sentiment_score > 0.05:
        overall_sentiment = "Positive"
    elif sentiment_score < -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    
    words = blob.words
    word_freq = {}
    for word in words:
        if len(word) > 3:
            word_freq[word.lower()] = word_freq.get(word.lower(), 0) + 1
    
    top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    top_keywords = [word for word, _ in top_keywords]
    
    return {
        "overallSentiment": overall_sentiment,
        "sentimentScore": sentiment_score,
        "topKeywords": top_keywords
    }