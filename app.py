import os
from dotenv.main import dotenv_values
from pymongo import MongoClient
from pprint import pprint
import certifi
from flask import Flask
from flask_restful import Resource, Api, reqparse

ca = certifi.where()

client = MongoClient(os.environ['MONGO_CONNECTION'], tlsCAFile=ca)
db=client.venues

def get_closest_venues(longitude, latitude, max):
    venues = list(db.venue.find({'loc.coord':{'$near':[longitude,latitude]}}).limit(max))
    retObject = {}
    for item in venues:
        for cat in item['categories']:
            if cat in retObject:
                retObject[cat]['venues'].append({'name': item['name'], 'address': item['address']})
            else:
                retObject.update({
                    cat: {
                        'category': cat,
                        'venues': [{'name': item['name'], 'address': item['address']}]
                    }
                })
    return  sorted(
                sorted(list(retObject.values()), key=lambda x: x['category'].lower()), key=lambda x: len(x['venues'])
            , reverse=True)

app = Flask(__name__)
api = Api(app)

class Venues(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('longitude', required=True)  # add arguments
        parser.add_argument('latitude', required=True)
        parser.add_argument('limit', required=False)

        args = parser.parse_args()  # parse arguments to dictionary

        max = args['limit'] if args['limit'] != None else 10

        return get_closest_venues(float(args['longitude']), float(args['latitude']), int(max)), 200
    pass

api.add_resource(Venues, '/')


if __name__ == "__main__":
    app.run()