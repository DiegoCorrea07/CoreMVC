from backend.models.user import User
from backend.models.event import Event
from backend.models.aircraft import Aircraft
from backend.models.route import Route
from backend.models.flight import Flight
from backend.models.demand import Demand
from backend.db.connection import db

def initialize_tables():
    with db:
        db.create_tables([User, Event, Aircraft, Route, Flight, Demand], safe=True)
