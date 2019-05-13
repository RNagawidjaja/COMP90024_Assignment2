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
    r = request.GET.get('p')
    parameter = check_request(r)

    data = {"latitude":-37.798805, "longitude":144.960839, "parameter": parameter}
    return render(None, "map.html", context=data)

# /geojson
def geojson(request):
    r = request.GET.get('p')
    parameter = check_request(r)
    (min, max) = get_min_max(parameter)

    url = 'http://45.113.233.237:5984/geojson/'

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
        feature = get_feature_1(id, url, parameter, min, max)
        features.append(feature)

    geo = {"type" : "FeatureCollection"}
    geo["features"] = features
    return JsonResponse(geo)


def check_request(r):
    parameter = 'exercise'
    if r == 'obesity':
        parameter = 'obesity'
    if r == 'alcohol':
        parameter = 'alcohol'
    if r == 'psych':
        parameter = 'psych'
    if r == 'exercise':
        parameter = 'exercise'
    if r == 'sloth':
        parameter = 'sloth'
    if r == 'gluttony':
        parameter = 'gluttony'
    return parameter


def get_min_max(parameter):
    url = 'http://45.113.233.237:5984/aurin_health_risk/_design/vic/_view/' + parameter
    if parameter == "sloth":
        url = 'http://45.113.233.237:5984/tweets/_design/geo/_view/sloth_rate?reduce=true&group_level=1'
    if parameter == "gluttony":
        url = 'http://45.113.233.237:5984/tweets/_design/geo/_view/gluttony_rate?reduce=true&group_level=1'

    response = urllib.request.urlopen(url).read()
    parsed = json.loads(response)

    values = None
    if parameter == "sloth" or parameter == "gluttony":
        values = [l['value']['sum'] / l['value']['count'] * 100 for l in parsed['rows']]
    else:
        values = [a['value'] for a in parsed['rows'] if a['value'] is not None]
    return min(values), max(values)


def get_feature_1(id, url, parameter, min_value, max_value):
    response = urllib.request.urlopen(url + str(id)).read()
    parsed = json.loads(response)

    properties = {}
    properties["id"] = "id="+str(id)
    properties.update(get_health_records_prop(id))
    properties.update(get_tweet_prop(id))

    reverse_map_color = False
    if parameter == 'sloth':
        reverse_map_color = True
    properties["color"] = get_color(min_value, max_value, properties[parameter], reverse_map_color)

    feature = {"type" : "Feature"}
    feature["properties"] = properties
    feature["geometry"] = parsed['geometry']
    return feature

def get_health_records_prop(id):
    url = 'http://45.113.233.237:5984/aurin_health_risk/'
    response = urllib.request.urlopen(url + str(id)).read()
    parsed = json.loads(response)

    properties = {}
    properties['alcohol'] = parsed['alchl_p_2_asr']
    properties['obesity'] = parsed['obese_p_2_asr']
    properties['psych'] = parsed['psych_dstrs_2_asr']
    properties['exercise'] = parsed['lw_excse_2_asr']

    return properties


def get_tweet_prop(id):
    properties = {'sloth': 0, 'gluttony': 0}
    url = "http://45.113.233.237:5984/tweets/_design/geo/_view/sloth_rate?reduce=true&group_level=1"
    response = urllib.request.urlopen(url).read()
    parsed = json.loads(response)
    for line in parsed['rows']:
        if line['key'] == str(id):
            properties["sloth"] = line['value']['sum'] / line['value']['count'] * 100
            break
    url = 'http://45.113.233.237:5984/tweets/_design/geo/_view/gluttony_rate?reduce=true&group_level=1'
    response = urllib.request.urlopen(url).read()
    parsed = json.loads(response)
    for line in parsed['rows']:
        if line['key'] == str(id):
            properties['gluttony'] = line['value']['sum'] / line['value']['count'] * 100
            break
    return properties


def get_color(min_value, max_value, value, reverse=False):
    colors = ["blue", "green", "yellow", "orange", "red"]
    if value == max_value:
        if reverse:
            return colors[0]
        return colors[-1]
    step = (max_value - min_value)/len(colors)
    i = int((value - min_value)/step)
    if reverse:
        i = len(colors) - i - 1
    return colors[i]
