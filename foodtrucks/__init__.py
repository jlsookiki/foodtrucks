from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hamlish_jinja import HamlishTagExtension
import yaml
app = Flask(__name__)
app.debug = True
app.config.from_pyfile('config.py')
app.jasmine_config = yaml.load('spec/javascripts/support/jasmine.yaml')

app.jinja_env.add_extension(HamlishTagExtension)

assets = Environment(app)
assets.url = app.static_url_path

css_bundle = Bundle('css/main.css', output='all.css')
assets.register('css_all', css_bundle)

js_bundle = Bundle('js/ext/jquery-2.1.3.js', 'js/ext/underscore.js', 'js/ext/backbone.js', 'js/ext/googlemaps.api.js', 'js/ext/backbone.googlemaps.js', 'js/foodtruckapp.js', 'js/main.js', output='all.js')
assets.register('js_all', js_bundle)

db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(engine)

session = Session()

from foodtrucks import views, models, utilities

