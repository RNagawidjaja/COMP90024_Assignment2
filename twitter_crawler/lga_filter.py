from shapely.geometry import Point
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
import json
import couchdb
import sys

class LGA_Filter:
    def __init__(self, lga_view):
        self._polygons = []
        for row in lga_view:
            polygon = []
            polygons = []
            try:
                type = row.value['geometry']['type']
                coordinates = row.value['geometry']['coordinates']
                id = row['id']
                if type == 'MultiPolygon':
                    for c in coordinates:
                        polygon = [tuple(l) for l in c[0]]
                        polygon = Polygon(polygon)
                        polygons.append(polygon)
                    multi_polygon = MultiPolygon(polygons)
                    self._polygons.append([id, multi_polygon])
                elif type == 'Polygon':
                    polygon = [tuple(l) for l in coordinates[0]]
                    polygon = Polygon(polygon)
                    self._polygons.append([id, polygon])
                else:
                    print('Incorrect type') 
            except KeyError:
                pass
            
    def filter(self, point):
        point = [point[1], point[0]]
        point = Point(tuple(point))
        
        for p in self._polygons:
            lga_id = None
            if p[1].contains(point):
                lga_id = p[0]
                break
            else:
                continue
        return lga_id
            

if __name__ == '__main__':
    #for testing
    #tweets_file = r'C:\Users\reyna\Documents\Unimelb\COMP90024\Assignment_2\tweets\tweets_coordinates.json'
    LGA_file = r'C:\Users\reyna\Documents\Unimelb\COMP90024\Assignment_2\tweets\LGA.json'
    
    #with open(tweets_file, encoding='UTF-8') as tf:
    #    tweets = json.load(tf)
    #y = tweets['rows'][0]['value']['coordinates']
    
    couchserver = couchdb.Server('http://45.113.233.19:8081')
    db_tweets = couchserver['tweets']
    db_tweets_geo = couchserver['tweets_geo']
    lga = LGA_Filter(LGA_file)
    for item in db_tweets.view('_design/geo/_view/geo', descending = True):
        lga_id = lga.filter(item.value['coordinates'])
        print(lga_id)
        #doc = {'_id': item.id, 'coordinates': item.value['coordinates'], 'lga_name' : lga_name}
        #try:
        #    db_tweets_geo.save(doc)
        #except couchdb.http.ResourceConflict:
        #    print(item.id)
        #    print('ID has already existed')
        #    sys.exit()
    
    #print(list(map(lga_f.filter, tweets['rows'])))