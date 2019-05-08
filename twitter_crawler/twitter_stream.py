# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from lga_filter import LGA_Filter
from topic_modelling import TopicModeller

import couchdb
import config
import json
 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self, db, locations, lga_filter, topic_modeller):
        self.db = db
        self.locations = locations
        self.lga_filter = lga_filter
        self.topic_modeller = topic_modeller

    def stream_tweets(self):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        auth = OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        listener = TwitterListener(self.db, self.lga_filter, self.topic_modeller)
        stream = Stream(auth, listener)

        # Fliter by location
        stream.filter(locations=self.locations)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, db, lga_filter, topic_modeller):
        self.db = db
        self.lga_filter = lga_filter
        self.topic_modeller = topic_modeller
        
    def on_data(self, data):
        topic = []
        try:
            tweet = json.loads(data)
            text = tweet['text']
            if tweet['geo'] != None:
                coordinates = tweet['geo']['coordinates']
                lga_id = self.lga_filter.filter(coordinates)
                tweet['lga_id'] = lga_id
            else:
                tweet['lga_id'] = None
            topic = self.topic_modeller.topic_of_tweet(text)
            tweet['topic'] = topic
            tweet['_id'] = tweet["id_str"]
            self.db.save(tweet)
        except couchdb.http.ResourceConflict:
            print("Document id " + tweet["id_str"] + " already in database")
        return True
          

    def on_error(self, status):
        print(status)
        if status == 420:
            # Returning false on_data method in case rate limit occurs
            return False
 
if __name__ == '__main__':
    try:
        loc = config.LOCATION
        couchserver = couchdb.Server("http://" + config.DATABASE_IP + ":" + config.DATABASE_PORT)

        db = couchserver[config.DATABASE_NAME]
        db_geojson = couchserver[config.DATABASE_LGA_NAME]
        db_geojson_view = db_geojson.view("_all_docs")

        lga_filter = LGA_Filter(db_geojson_view)
        topic_modeller = TopicModeller()
        twitter_streamer = TwitterStreamer(db, loc, lga_filter, topic_modeller)
        twitter_streamer.stream_tweets()
    except KeyboardInterrupt:
        print("\nQuiting")
        exit()
