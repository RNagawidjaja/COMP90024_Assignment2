# COMP90024 Cloud and Cluster Computing
# Team 77 - Melbourne
# Uploads a json file with tweets to a couchdb server

import json
import couchdb
import re
from lga_filter import LGA_Filter
from topic_modelling import TopicModeller

server = couchdb.Server('http://172.26.38.67:5984')
tweets = server["tweets"]

serverg = couchdb.Server('http://45.113.233.237:5984')
geojson = serverg["geojson"]
geojson_view = geojson.view("_design/geojsonview/_view/geojsonview")
lga = LGA_Filter(geojson_view)

topic_modeller = TopicModeller()

with open("./tinyTwitter.json") as file:
    for i, line in enumerate(file):
        if i == 0:
            continue
        if i > 100:
            break
        line = re.sub(",\s*$", "", line)
        tweet = json.loads(line)
        text = tweet['doc']['text']
        if tweet["doc"]["geo"]["coordinates"] != None:
            coordinates = tweet["doc"]["geo"]["coordinates"]
            lga_id = lga.filter(coordinates)
            tweet['doc']['lga_id'] = lga_id
        else:
            tweet['doc']['lga_id'] = None
        topic = topic_modeller.topic_of_tweet(text)
        tweet['doc']['topic'] = topic
        del tweet['doc']['_rev']
        try:
            tweets.save(tweet['doc'])
        except:
            pass