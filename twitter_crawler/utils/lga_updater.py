from lga_filter import LGA_Filter

import json
import couchdb

server = couchdb.Server('http://45.113.233.237:5984')
tweets = server["tweets"]
geojson = server["geojson"]

geojson_view = geojson.view("_design/geojsonview/_view/geojsonview")
lga = LGA_Filter(geojson_view)
count = 1

for row in tweets.view("_design/noLGAField/_view/noLGAField"):
    doc = tweets.get(row["id"])
    coordinates = row["value"]["coordinates"]
    lga_id = lga.filter(coordinates)
    doc["lga_id"] = lga_id
    tweets.save(doc)

    print(count)
    count += 1
