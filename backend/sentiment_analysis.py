from textblob import TextBlob
import yake
kw_extractor = yake.KeywordExtractor()
language = "en"
max_ngram_size = 3
deduplication_threshold = 0.2
numOfKeywords = 20
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    
    if sentiment_score > 0.05:
        overall_sentiment = "Positive"
    elif sentiment_score < -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    
    keywords = custom_kw_extractor.extract_keywords(text)
    top_keywords = [keyword[0] for keyword in keywords]
    
    return {
        "overallSentiment": overall_sentiment,
        "sentimentScore": sentiment_score,
        "topKeywords": top_keywords
    }

results = analyze_sentiment("john is a computer science graduate with skills in programming and years of experience under his belt. he is a hard worker and is a team player")
print(results)