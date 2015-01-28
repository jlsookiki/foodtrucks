from foodtrucks.models import FoodTruck
from foodtrucks import session, services, db


def seed_db():
    data = services.fetch_trucks()
    for truck in data:
        session.add(FoodTruck(truck))
    commit = session.commit()


