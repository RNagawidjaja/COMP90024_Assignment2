# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy import API
from tweepy import Cursor #use for iterating through multiple tweets
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream  #streaming API of twittter

import re
import twitter_credentials #file containing Consumer and API keys
from couchdb import CouchDB

# TWITTER CLIENT

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        
        self.twitter_user = twitter_user
        
    def get_twitter_client_api(self):
        return self.twitter_client
        
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets): #twitter_client is a internal variable of Cursor
            tweets.append(tweet)
        return tweets
            
        
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
        
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(self.num_tweets):
            home_timeline.append(tweet)
        return home_timeline
        
        
    def search_tweet(self, q_search, loc_search):
        tweets = []
        with open('tweets_search.json', 'a', encoding='UTF-8') as tf:
            for tweet in Cursor(self.twitter_client.search, q=q_search, geocode=loc_search).items():
                tf.write(str(tweet) + '\n')
        return True
        
# # # # TWITTER AUTHENTICATOR # # #

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth
 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list, locations):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        auth = self.twitter_authenticator.authenticate_twitter_app()
        listener = TwitterListener(fetched_tweets_filename)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list, locations=locations)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            couchdb = CouchDB("45.113.233.19", "8081", "tweets")
            couchdb.saveTweet(data)
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        if status == 420:
            
            #Returning false on_data method in case rate limit occurs
            return False
        print(status)

 
if __name__ == '__main__':
    hash_tag_list = []
    q_search = "*"
    loc_stream = [144.5532, -38.2250, 145.5498, -37.5401, 150.6396, -34.1399, 151.3439, -33.5780] #Melbourne, Sydney
    loc_melb = "-37.8658,145.1028,30km"
    loc_syd = "-33.8563,151.0210,30km"
    fetched_tweets_filename = 'tweets_stream.json'
    twitter_client = TwitterClient()
    #twitter_client.search_tweet(q_search, loc_melb)
    #twitter_client.search_tweet(q_search, loc_syd)
        
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list, loc_stream)
