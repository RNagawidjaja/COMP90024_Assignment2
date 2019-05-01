from django.shortcuts import render
from django.http import HttpResponse
import json
import urllib.request

from django.http import JsonResponse

# Create your views here.
# /index
def index(request):
    return render(None, "index.html")

# /map
def map(request):
    data = {"latitude":-37.798805, "longitude":144.960839}
    return render(None, "map.html", context=data)


def geojson(request):
    url = 'http://45.113.233.19:8081/geojson/'

    ids = [
	20660, 20910,
	21110, 21180, 21610, 21890,
	22170, 22310, 22670, 22750,
	23110, 23270, 23430, 23670,
	24210, 24330, 24410, 24600, 24650, 24970,
	25060, 25250, 25340, 25710, 25900,
	26350, 26980,
	27070, 27260, 27350,
    ]
    features = []
    for i, id in enumerate(ids):
        feature = get_feature(id, i, url)
        features.append(feature)

    geo = {"type" : "FeatureCollection"}
    geo["features"] = features
    return JsonResponse(geo)

# /allgeojson
def allgeojson(request):
    url = 'http://45.113.233.19:8081/geojson/'
    response = urllib.request.urlopen(url + '_all_docs').read()
    parsed = json.loads(response)
    docs = parsed['rows']

    features = []
    for i, doc in enumerate(docs):
        id = doc['id']
        feature = get_feature(id, i, url)
        features.append(feature)

    geo = {"type" : "FeatureCollection"}
    geo["features"] = features
    return JsonResponse(geo)

def get_feature(id, i, url):
    colors = ["green", "red", "blue", "yellow", "orange", "DodgerBlue", "SlateBlue"]

    response = urllib.request.urlopen(url + str(id)).read()
    parsed = json.loads(response)

    feature = {"type" : "Feature"}
    properties = {}
    properties["color"] = colors[i % len(colors)]
    properties["id"] = "id="+str(id)
    properties["health_records"] = get_health_records_prop(id)
    feature["properties"] = properties
    feature["geometry"] = parsed['geometry']
    return feature

def get_health_records_prop(id):
    url = 'http://45.113.233.19:8081/aurin/'
    response = urllib.request.urlopen(url + str(id)).read()
    parsed = json.loads(response)

    return parsed['admis_mental_hlth_rltd_cond_p_all_hosps_2016_17_num']
