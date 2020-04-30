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

class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        """
        self.client.user_timeline gets the timeline tweets from the authenticated user,
        it can also get timeline tweets from another user if specified
        Cursor().items(num) returns num tweets from user timeline
        """
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client, id=self.twitter_user).items(num_friends):
             friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()


    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # filter adds tweets to a stream that contain any string in track
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    """
    Basic listener class that prints received tweets to stdout
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    # overwriting from StreamListener class
    # takes in data read from StreamListener
    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    # overwriting from StreamListener class
    # takes in error message
    def on_error(self, status):
        if status == 420:
            # Return False on_data method in case rate limit is met
            return False
        print(status)

class TweetAnalyzer():
    """
    Class analyzes and categorizes content from tweets
    """
    def clean_tweet(self, tweet):
        # Removes special characters from a tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1 # positive tweet
        elif analysis.sentiment.polarity == 0:
            return 0 # neutral tweet
        else:
            return -1 # negative tweet

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets]) # iphone, android, desktop, etc.
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=20)
    # prints id of a tweet
    #print(tweets[0].id)
    #print(tweets[0].retweet_count)
    # prints attribute values of tweet object
    #print(dir(tweets[0]))
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    #print(df.head(10))
    # print("size: ", len(df))
    # Get average length over all tweets
    # print(np.mean(df['len']))

    # Time series
    # time_likes = pd.Series(df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16,4), color='r')
    # plt.show()

    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    print(df.head(10))
