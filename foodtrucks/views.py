import json
from foodtrucks import app, utilities, session
from foodtrucks.models import FoodTruck
from geoalchemy2 import shape
from shapely.geometry import Polygon
from flask import request
from flask import render_template, Response


@app.route('/')
def index():
    return render_template('index.html.haml')

@app.route('/refresh')
def refresh_data():
    truck = utilities.seed_db()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/trucks/area')
def trucks_by_area():
    bounds = request.args
    x1 = float(bounds['bound1[x]'])
    y1 = float(bounds['bound1[y]'])
    x2 = float(bounds['bound2[x]'])
    y2 = float(bounds['bound2[y]'])
    sf1 = shape.from_shape(Polygon([(x1, x2), (x1, y2), (x2, y1), (x2, y2)]))
    results = session.query(FoodTruck).filter(FoodTruck.location.intersects(sf1)).all()
    trucks = map(lambda x: x.to_dict(), results)

    #Flask jsonify won't return an array for security reasons(?)
    return Response(json.dumps(trucks), mimetype='application/json')