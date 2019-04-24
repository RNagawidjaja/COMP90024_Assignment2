# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy import API
from tweepy import Cursor #use for iterating through multiple tweets
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream  #streaming API of twittter
from tweepy import error
from couchdb import CouchDB

import config #file containing Consumer and API keys
import time
import json

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        self.auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def search_tweet(self, db, q_search, loc_search):
        for tweet in Cursor(self.twitter_client.search,
                            q=q_search, geocode=loc_search,
                            wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items():
            id = tweet.id
            db.saveJson(id, tweet._json)

if __name__ == '__main__':
    q_search = "*"
    loc_melb = "-37.8658,145.1028,50km"
    loc_syd = "-33.8563,151.0210,50km"
    twitter_client = TwitterClient()
    db = CouchDB(config.DATABASE_IP, config.DATABASE_PORT, config.DATABASE_NAME)

    while True:
        try:
            twitter_client.search_tweet(db, q_search, loc_melb)
            #twitter_client.search_tweet(db, q_search, loc_syd)
        except KeyboardInterrupt:
            print("\nQuiting")
            exit()