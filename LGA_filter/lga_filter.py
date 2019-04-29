from shapely.geometry import Point
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
import json
from numpy import array

class LGA_filter:
    def __init__(self, lga_file):
        with open(LGA_file, encoding='UTF-8') as lf:
            self.lga = json.load(lf)
            
    def filter(self, tweet):
        point = tweet['value']['coordinates']
        point = [point[1], point[0]]
        point = Point(tuple(point))
        lga_name = None
        for row in self.lga['rows']:
            coordinates = row['doc']['geometry']['coordinates']
            type = row['doc']['geometry']['type']
            polygons = []
            if type == 'MultiPolygon':
                for c in coordinates:
                    polygon = [tuple(l) for l in c[0]]
                    polygon = Polygon(polygon)
                    polygons.append(polygon)
                multi_polygon = MultiPolygon(polygons)
                if multi_polygon.contains(point):
                    lga_name = row['doc']['lga_name']
                    break
                else:
                    continue
            elif type == 'Polygon':
                polygon = [tuple(l) for l in coordinates[0]]
                polygon = Polygon(polygon)
                if polygon.contains(point):
                    lga_name = row['doc']['lga_name']
                    break
                else:
                    continue
            else:
                print('Incorrect type')
        return lga_name
            

if __name__ == '__main__':
    tweets_file = r'C:\Users\reyna\Documents\Unimelb\COMP90024\Assignment_2\tweets\tweets_coordinates.json'
    LGA_file = r'C:\Users\reyna\Documents\Unimelb\COMP90024\Assignment_2\tweets\LGA.json'
    
    with open(tweets_file, encoding='UTF-8') as tf:
        tweets = json.load(tf)
    #y = tweets['rows'][0]['value']['coordinates']
    
    lga_f = LGA_filter(LGA_file)
    print(list(map(lga_f.filter, tweets['rows'])))