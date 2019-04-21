import requests
import json

class CouchDB:

    def __init__(self, ip, port, db):
        self.ip = ip
        self.port = port
        self.serverURL = "http://" + ip + ":" + port
        self.db = db

    def getDBs(self):
        url =  self.serverURL + "/_all_dbs"
        res = requests.get(url)
        return res.json()

    def saveJson(self, id, data):
        url =  self.serverURL + "/" + self.db + "/" + id
        res = requests.put(url, data=json.dumps(data))
        return res.json()

if __name__ == '__main__':
    # For testing
    couchdb = CouchDB("45.113.233.19", "8081", "testing")
    
    data = json.loads('{"id_str":"1", "Name":"Raju", "age":23, "Designation":"Designer"}')
    id = data["id_str"]

    print(couchdb.getDBs())
    print(couchdb.saveJson(id, data))