from textblob import TextBlob
import yake
kw_extractor = yake.KeywordExtractor()
language = "en"
max_ngram_size = 3
deduplication_threshold = 0.2
numOfKeywords = 20
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)

def analyze_sentiment(text):
    '''https://textblob.readthedocs.io/en/dev/quickstart.html'''
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    
    if sentiment_score > 0.05:
        overall_sentiment = "Positive"
    elif sentiment_score < -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    
    '''https://towardsdatascience.com/keyword-extraction-process-in-python-with-natural-language-processing-nlp-d769a9069d5c'''
    keywords = custom_kw_extractor.extract_keywords(text)
    top_keywords = [keyword[0] for keyword in keywords]
    
    return {
        "overallSentiment": overall_sentiment,
        "sentimentScore": sentiment_score,
        "topKeywords": top_keywords
    }

results = analyze_sentiment("lazy and diligent")
print(results)