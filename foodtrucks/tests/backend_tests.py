import os
import foodtrucks
from foodtrucks import app, db
import unittest
import tempfile
import httpretty
import json

class FoodtrucksTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, foodtrucks.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app
        db.create_all()
        self.data = {'status': 'status', 'foodItems': 'items', 'facilitytype': 'test',
                                             'location': {'latitude': 37.768903534358, 'longitude': -122.415981174592}, 'scheduleURL': 'test', 'applicant': 'owner'}
        self.truck = foodtrucks.models.FoodTruck(self.data)
        uri = self.app.config.get('SF_DATA_BASE_URL')
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, uri, body=json.dumps([self.data]))

    def tearDown(self):
        db.session.remove()
      #  db.drop_all()
        db.session.query(foodtrucks.models.FoodTruck).delete()
        db.session.commit()
        httpretty.disable()
        httpretty.reset()

    #test services
    def test_services_fetch_trucks(self):

        response = foodtrucks.services.fetch_trucks()

        self.assertEquals(response, [self.data])

    #test utilities
    def test_seed_db(self):
        all = foodtrucks.models.FoodTruck.query.count()
        self.assertEquals(all, 0)
        truck = foodtrucks.utilities.seed_db()
        all = foodtrucks.models.FoodTruck.query.count()
        self.assertEqual(all, 1)
        truck = foodtrucks.utilities.seed_db()
        all = foodtrucks.models.FoodTruck.query.count()
        self.assertEqual(all, 2)

    #test models
    def test_foodtruck_to_dict(self):
        dict = {'status': 'status', 'foodItems': '', 'lat': 37.7689035344, 'scheduleURL': '', 'lng': -122.415981175, 'type': 'test', 'id': None, 'owner': 'owner'}

        self.assertEquals(self.truck.to_dict(), dict)

    def test_foodtruck_repr(self):
        repr = "status: status, foodItems: , type: test, location: Point(37.7689035344 -122.415981175), scheduleURL: , owner: owner"

        self.assertEquals(str(self.truck), repr)

    #test views
    def test_index(self):
        client = app.test_client(self)
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_refresh_data(self):
        client = app.test_client(self)
        response = client.get('/refresh')
        self.assertEqual(response.status_code, 200)

    def test_trucks_by_area_success(self):
        client = app.test_client(self)
        response = client.get('/trucks/area?bound1%5Bx%5D=37.844405931964936&bound1%5By%5D=37.70960661894275&bound2%5Bx%5D=-122.47459342370604&bound2%5By%5D=-122.36146857629393')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data), 1)

    def test_trucks_by_area_fail(self):
        client = app.test_client(self)
        response = client.get('/trucks/area?bound1%5Bx%5D=0&bound1%5By%5D=0&bound2%5Bx%5D=5&bound2%5By%5D=5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data), 0)