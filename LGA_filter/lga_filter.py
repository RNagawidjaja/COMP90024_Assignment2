from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json


if __name__ == '__main__':
    tweets_file = r'C:\Users\reyna\Documents\Unimelb\COMP90024\Assignment_2\tweets\tweets_coordinates.json'
    LGA_file = r'C:\Users\reyna\Documents\Unimelb\COMP90024\Assignment_2\tweets\LGA.json'
    with open(LGA_file, encoding='UTF-8') as lf:
        lga = json.load(lf)
        
    x = lga['rows'][0]['doc']['geometry']['coordinates'][0][0]
    x = [tuple(l) for l in x]
    print(x)
    with open(tweets_file, encoding='UTF-8') as tf:
        tweets = json.load(tf)
        
    polygon = Polygon(x)
    y = tweets['rows'][0]['value']['coordinates']
    y = tuple(y)
    point = Point(y)
    print(polygon.contains(point))
        