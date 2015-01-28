from foodtrucks import db, session
from geoalchemy2.types import Geometry
from geoalchemy2 import WKTElement
from sqlalchemy import func
import json


class FoodTruck(db.Model):

    __tablename__ = 'foodtruck'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    foodItems = db.Column(db.String)
    type = db.Column(db.String)
    location = db.Column(Geometry("POINT"))
    scheduleURL = db.Column(db.String)
    owner = db.Column(db.String)

    def __init__(self, truck):
        self.status = truck.get('status','')
        self.foodItems = truck.get('fooditems','')
        self.type = truck.get('facilitytype','Unknown')
        loc = truck.get('location', '')
        if loc:
            geo = WKTElement('Point(%s %s)' % (loc.get('latitude', 0), loc.get('longitude', 0)))
            self.location = geo
        self.scheduleURL = truck.get('schedule','')
        self.owner = truck.get('applicant','')

    def __repr__(self):
        return "status: %s, foodItems: %s, type: %s, location: %s, scheduleURL: %s, owner: %s" % (self.status, self.foodItems, self.type, self.location, self.scheduleURL, self.owner)

    def to_dict(self):
        location = json.loads(session.scalar(func.ST_AsGeoJSON(self.location)))['coordinates']
        return {
            "id": self.id,
            "status": self.status,
            "foodItems": self.foodItems,
            "type": self.type,
            "lat": location[0],
            "lng": location[1],
            "scheduleURL": self.scheduleURL,
            "owner": self.owner
        }