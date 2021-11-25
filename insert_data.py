from pymongo import GEO2D, GEOSPHERE, MongoClient
from pprint import pprint
import csv
import sys
import certifi
from dotenv.main import dotenv_values

ca = certifi.where()

config = dotenv_values('.env')

client = MongoClient(config['MONGO_CONNECTION'], tlsCAFile=ca)
db=client.venues

dataFile = str(sys.argv[1]) if len(sys.argv) > 1 else 'venues.csv'

with open(dataFile, newline='') as csvfile:
    venueReader = csv.reader(csvfile, delimiter=',')
    for row in venueReader:
        if row[0] == 'name':
            continue
        item = {}
        item.update({"name": row[0]})
        item.update({"address": row[1]})
        item.update({"categories": list(filter(lambda val: '$' not in val, row[2].split(',')))})
        item.update({
            "loc": {
                "type": "Point",
                "coord": [float(row[4]), float(row[3])]
            }
        })
        try:
            print("Inserting: ")
            pprint(item)
            venues = db.venue
            venues.insert_one(item)
        except:
            print("Failed to insert: ")
            pprint(item)

venue = db.venue
venue.drop_indexes()
venue.create_index([('loc.coord', GEOSPHERE)],name='sphere2dcoord')
venue.create_index([('loc.coord', GEO2D)],name='flat2dcoord')
print("Created indexes:")
pprint(venue.index_information())