from topic_modelling import TopicModeller

import json
import couchdb

server = couchdb.Server('http://45.113.233.237:5984')
tweets = server["tweets"]

topic_modeller = TopicModeller()

count = 1

for row in tweets.view("_design/noTopic/_view/noTopic"):
    doc = tweets.get(row["id"])
    text = doc["text"]
    topic = topic_modeller.topic_of_tweet(text)
    doc["topic"] = topic
    tweets.save(doc)

    print(count)
    count += 1
