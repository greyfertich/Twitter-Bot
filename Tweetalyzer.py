from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter_credentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Tweetalyzer():

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # Authenticate user
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

    def get_tweets_by_user(user, count=10):
        pass

    def get_tweets_by_keyword(user, count=10):
        tweets = apt.search('Trump')
        return tweets

















if __name__ == '__main__':
    consumer_key = twitter_credentials.CONSUMER_KEY
    consumer_secret = twitter_credentials.CONSUMER_SECRET
    access_token = twitter_credentials.ACCESS_TOKEN
    access_token_secret = twitter_credentials.ACCESS_TOKEN_SECRET
    analyzer = Tweetalyzer(consumer_key, consumer_secret, access_token, access_token_secret)
    print(len(tweets))
