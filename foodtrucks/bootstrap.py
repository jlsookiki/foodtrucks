import config, os, sqlalchemy, imp
from sqlalchemy import create_engine
from foodtrucks import app,db
from migrate.versioning import api
from geoalchemy2 import Geometry
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

#Check if database exists, and create it if it does not
engine = create_engine(SQLALCHEMY_DATABASE_URI)
try:
    engine.connect()
    print 'connected'
except sqlalchemy.exc.OperationalError:
    print 'failed to connect, creating'
    engine = create_engine("postgresql://%s:%s@localhost/postgres" % (config.DB_USER, config.DB_PASS))
    conn = engine.connect()
    conn.execute('commit')
    conn.execute('create database %s' % (config.DB_NAME))
    conn.close()
    #add in postgis for geolocation
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    conn = engine.connect()
    conn.execute('create extension postgis')
    conn.close()

db.create_all()