import json
import urllib
import urllib2
from foodtrucks import db, app

def fetch_trucks(options={}):
    SF_DATA_URL = app.config.get('SF_DATA_BASE_URL')
    response = urllib2.urlopen(SF_DATA_URL)
    foodTrucks = json.load(response)

    return foodTrucks