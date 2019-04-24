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

# TWITTER CLIENT

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        self.auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def search_tweet(self, db, q_search, loc_search, max_id):
        for tweet in Cursor(self.twitter_client.search, q=q_search, geocode=loc_search, max_id = max_id, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items(30):
            id = tweet.id
            db.saveJson(id, tweet._json)
        return id


if __name__ == '__main__':
    hash_tag_list = []
    q_search = "*"
    loc_melb = "-37.8658,145.1028,30km"
    loc_syd = "-33.8563,151.0210,30km"
    twitter_client = TwitterClient()
    count = 0
    max_id_melb = 9999999999999999999
    max_id_syd = 9999999999999999999
    min_id_melb = 1118302967764013059 #min id on 17/4/2019
    min_id_syd = 1118302964962209792 #min id on 17/4/2019
    db = CouchDB(config.DATABASE_IP, config.DATABASE_PORT, config.DATABASE_NAME)

    while True:
        if min_id_melb >= max_id_melb or min_id_syd >= max_id_syd:
            time.sleep(6*60*60)
            #print('min id reached')
            max_id_melb = 9999999999999999999
            max_id_syd = 9999999999999999999
            min_id_melb = twitter_client.search_tweet(q_search, db, loc_melb, max_id_melb)
            min_id_melb = twitter_client.search_tweet(q_search, db, loc_syd, max_id_syd)
        max_id_melb = twitter_client.search_tweet(q_search, db, loc_melb, max_id_melb)
        max_id_syd = twitter_client.search_tweet(q_search, db, loc_syd, max_id_syd)
        if count >= 28:
            #print('sleep time')
            time.sleep(15*60)

            count = 0
        else:
            count = count + 1