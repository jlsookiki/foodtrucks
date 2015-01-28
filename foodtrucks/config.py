import os

SQLALCHEMY_DATABASE_URI = "postgressql://localhost"
SF_DATA_BASE_URL = "https://data.sfgov.org/resource/rqzj-sfat.json"

DB_USER = 'foodtruck'
DB_PASS = 'ftdb'
DB_NAME = 'foodtrucks'

#Config needed to start the database
SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@localhost/%s" % (DB_USER, DB_PASS, DB_NAME)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
