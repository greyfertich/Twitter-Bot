from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter_credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
import re

class Tweetalyzer():

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # Authenticate user
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.twitter_client = API(self.auth)

    def get_tweets_by_user(self, user, count=10):
        pass

    def get_tweets_by_keyword(self, user, count=10):
        return self.twitter_client.search('Trump', count=count)

    def analyze_sentiment(self, tweet):
        return TextBlob(self.clean_tweet(tweet)).sentiment

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())








if __name__ == '__main__':
    consumer_key = twitter_credentials.CONSUMER_KEY
    consumer_secret = twitter_credentials.CONSUMER_SECRET
    access_token = twitter_credentials.ACCESS_TOKEN
    access_token_secret = twitter_credentials.ACCESS_TOKEN_SECRET
    analyzer = Tweetalyzer(consumer_key, consumer_secret, access_token, access_token_secret)
    tweets = analyzer.get_tweets_by_keyword(None)
    for tweet in tweets:
        print(tweet.text, "Sentiment: {}\n\n".format(analyzer.analyze_sentiment(tweet.text)))
    print("Printed all {} tweets".format(len(tweets)))
