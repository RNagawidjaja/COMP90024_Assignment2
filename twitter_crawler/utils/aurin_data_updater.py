import json
import couchdb

server = couchdb.Server('http://45.113.233.237:5984')
website = server["website"]

# Change file name to aurin data file downloaded
# with open("data.json") as file:
#     aurin_data = json.load(file)

count = 1

for row in website.view("_all_docs"):
    doc_id = row["id"]
    doc = website.get(doc_id)
    # Change props to include what data we want to show
    props = {"Test" : "test value"}
    doc["properties"] = {**doc["properties"], **props}
    website.save(doc)

    # Show progress when running
    print(count)
    count += 1