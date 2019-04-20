import requests
import json

class CouchDB:

    def __init__(self, ip, port, db):
        self.server = "http://" + ip + ":" + port
        self.db = db

    def getDBs(self):
        url =  self.server + "/_all_dbs"
        res = requests.get(url)
        return res.text

    def saveTweet(self, tweet):
        url =  self.server + "/" + self.db + "/"
        tweetJson = json.loads(tweet)
        res = requests.put(url + tweetJson["id_str"], data=json.dumps(tweetJson))
        return res.text

if __name__ == '__main__':
    couchdb = CouchDB("45.113.233.19", "8081", "tweets")
    print(couchdb.getDBs())
    print(couchdb.saveTweet('{"id_str":"1", "Name":"Raju", "age":23, "Designation":"Designer"}'))