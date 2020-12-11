import tweepy
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('',
                      '')

api = tweepy.API(auth)
public_tweets = api.search('2020')
twitterHandle = 'JoeBiden'
tweetCount = 30

tweets = api.user_timeline(screen_name=twitterHandle,
                           # 200 is the maximum allowed count
                           count=tweetCount,
                           include_rts=True,
                           # Necessary to keep full_text
                           # otherwise only the first 140 words are extracted
                           tweet_mode='extended'
                           )
polarity = 0
subjectivity = 0
count = 0;
for info in tweets:
    analysis = TextBlob(info.full_text)
    polarity = polarity + analysis.sentiment.polarity
    subjectivity = subjectivity + analysis.sentiment.subjectivity

print(polarity / tweetCount)
print(subjectivity / tweetCount)

blob = TextBlob(tweets[0].full_text, analyzer=NaiveBayesAnalyzer())
print("Text Blob")
print(blob.sentiment)
score = analyser.polarity_scores((tweets[0].full_text))
print("Vader")
print(str(score))
