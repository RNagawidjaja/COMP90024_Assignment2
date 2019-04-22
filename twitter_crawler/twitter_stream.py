# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from couchdb import CouchDB

import config
import json
 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self, db, locations):
        self.db = db
        self.locations = locations

    def stream_tweets(self):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        listener = TwitterListener(self.db)
        stream = Stream(auth, listener)

        # Fliter by location
        stream.filter(locations=self.locations)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, db):
        self.db = db

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            id = tweet["id_str"]
            res = self.db.saveJson(id, tweet)
            if "error" in res and res["error"] == "conflict":
                print("Document id " + id + " already in database")
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        print(status)
        if status == 420:
            # Returning false on_data method in case rate limit occurs
            return False
 
if __name__ == '__main__':
    loc = config.LOCATION
    db = CouchDB(config.DATABASE_IP, config.DATABASE_PORT, config.DATABASE_NAME)
    twitter_streamer = TwitterStreamer(db, loc)
    twitter_streamer.stream_tweets()
