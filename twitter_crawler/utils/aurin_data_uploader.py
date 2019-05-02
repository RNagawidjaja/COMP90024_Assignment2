import json
import couchdb

server = couchdb.Server('http://45.113.233.237:5984')
geojson = server["geojson"]
website = server["website"]

# Change file name to aurin data file downloaded
with open("data.json") as file:
    aurin_data = json.load(file)

count = 0

for row in geojson.view("_design/geojsonview/_view/geojsonview"):
    geo_doc = row["value"]

    # Change props to include what data we want to show
    props = {"LGA Code" : geo_doc["id"], "LGA Name" : geo_doc["lga_name"]}
    doc = {"type" : "Feature", "geometry" : geo_doc["geometry"], "properties" : props}
    website.save(doc)

    # Show progress when running
    print(count)
    count += 1
